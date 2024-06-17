
from machine import Pin, I2C, ADC, PWM, Timer
import network
import time
import socket
import math


            
class myclient():

    def __init__(self, host, port): # Initialises all the data needed to connect to the server
        self.host = host
        self.port = port
        self.mydataout = ""
        self.mydatain = ""
        self.finaldeng = 0
        self.mySocket = None
        self.connect()

    def connect(self):
        try:
            print("Connecting to", self.host, self.port) 
            self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialises socket to communicate with the server
            self.mySocket.connect((self.host, self.port))
        except Exception as e:
            print("Connection Error:", e)
            self.mySocket.close()
            time.sleep(1)
            self.connect()

    def senddata(self, datatosend, number): # function to use socket in order to send data to server
        try:
            self.mydataout = datatosend
            self.mySocket.send(self.mydataout.encode())
            print("Sent:", self.mydataout)

            self.mydatain = self.mySocket.recv(1024).decode()
            print("Received:", self.mydatain)

            if self.mydataout.upper() == self.mydatain:
                print("Data received ok")
                self.mydataout = str(number)
                self.mySocket.send(self.mydataout.encode())
                print("Sent:", self.mydataout)
                self.mydatain = self.mySocket.recv(1024).decode()
                print("Received:", self.mydatain)

                self.finaldeng = self.mydatain
            else:
                print("Data error")
        except Exception as e:
            print("Send/Receive Error:", e)
            self.connect()

    def close(self): # close connection with the server to let others communicate with server
        print("Closing socket")
        self.mySocket.close()

def connectwifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)  # Connects to given SSID nework
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to WiFi')

SSID = 'Sophie'
PASSWORD = 'EEE123EEE'
connectwifi(SSID, PASSWORD)

data = 0 # data to be sent to server       
previous = 0 # used to find the derivative of the error by storing previous error
diff = 0 # derivative of error
# Set up some pin allocations for the Analogues and switches
va_pin = ADC(Pin(28))
vb_pin = ADC(Pin(26))
vpot_pin = ADC(Pin(27))
OL_CL_pin = Pin(12, Pin.IN, Pin.PULL_UP)
BU_BO_pin = Pin(2, Pin.IN, Pin.PULL_UP)

# Set up the I2C for the INA219 chip for current sensing
ina_i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=2400000)

# Some PWM settings, pin number, frequency, duty cycle limits and start with the PWM outputting the default of the min value.
pwm = PWM(Pin(9))
pwm.freq(100000)
min_pwm = 1000
max_pwm = 64536
pwm_out = min_pwm
pwm_ref = 30000

#Some error signals
trip = 0
OC = 0


# The potentiometer is prone to noise so we are filtering the value using a moving average
v_pot_filt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
v_pot_index = 0

# Gains etc for the PID controller
v_ref = 0 # Voltage reference for the CL modes
v_err = 0 # Voltage error
v_err_int = 0 # Voltage error integral
i_pi_out = 0 # Output of the voltage PI controller
kp = 20 # Proportional Gain tuned
ki = 30 # Integral Gain tuned
BUS = 15 # Desired Bus Voltage that we want to control

slide = 0
# Basic signals to control logic flow
global timer_elapsed, count
timer_elapsed = 0
count = 0
first_run = 1

# Need to know the shunt resistance
global SHUNT_OHMS
SHUNT_OHMS = 0.10

#Initialize other variables


#Initialize loop_counters

# saturation function for anything you want saturated within bounds

def saturate(signal, upper, lower):  #sets the signal between max and min
    if signal > upper:
        signal = upper
    if signal < lower:
        signal = lower
    return signal


# This is the function executed by the loop timer, it simply sets a flag which is used to control the main loop
def tick(t): 
    global timer_elapsed
    timer_elapsed = 1

# These functions relate to the configuring of and reading data from the INA219 Current sensor
class ina219: 
    
    # Register Locations
    REG_CONFIG = 0x00
    REG_SHUNTVOLTAGE = 0x01
    REG_BUSVOLTAGE = 0x02
    REG_POWER = 0x03
    REG_CURRENT = 0x04
    REG_CALIBRATION = 0x05
    
    def __init__(self,sr, address, maxi):
        self.address = address
        self.shunt = sr
            
    def vshunt(icur):
        # Read Shunt register 1, 2 bytes
        reg_bytes = ina_i2c.readfrom_mem(icur.address, icur.REG_SHUNTVOLTAGE, 2)
        reg_value = int.from_bytes(reg_bytes, 'big')
        if reg_value > 2**15: #negative
            sign = -1
            for i in range(16): 
                reg_value = (reg_value ^ (1 << i))
        else:
            sign = 1
        return (float(reg_value) * 1e-5 * sign)
        
    def vbus(ivolt):
        # Read Vbus voltage
        reg_bytes = ina_i2c.readfrom_mem(ivolt.address, ivolt.REG_BUSVOLTAGE, 2)
        reg_value = int.from_bytes(reg_bytes, 'big') >> 3
        return float(reg_value) * 0.004
        
    def configure(conf):

        ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x19\x9F') # PG = /8
        ina_i2c.writeto_mem(conf.address, conf.REG_CALIBRATION, b'\x00\x00')




while True: # Code to be executed at all the times
    if first_run:
        
        # for first run, set up the INA link and the loop timer settings
        ina = ina219(SHUNT_OHMS, 64, 5)
        ina.configure()
        first_run = 0
        
        # This starts a 1kHz timer which we use to control the execution of the control loops and sampling
        loop_timer = Timer(mode=Timer.PERIODIC, freq=1000, callback=tick)
    
    # If the timer has elapsed it will execute some functions, otherwise it skips everything and repeats until the timer elapses
    if timer_elapsed == 1: # This is executed at 1kHz
        va = 1.017*(12490/2490)*3.3*(va_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
        vb = 1.015*(12490/2490)*3.3*(vb_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
        
        
        vpot_in = 1.026*3.3*(vpot_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
        v_pot_filt[v_pot_index] = vpot_in # Adds the new reading to our array of readings at the current index
        v_pot_index = v_pot_index + 1 # Moves the index of the buffer for next time
        if v_pot_index == 100: # Loops it round if it reaches the end
            v_pot_index = 0
        vpot = sum(v_pot_filt)/100 # Actual reading used is the average of the last 100 readings
        
        Vshunt = ina.vshunt()
        CL = OL_CL_pin.value() # Pin to read if we are in open or closed loop
        BU = BU_BO_pin.value() # Pin to read if we are in buck or boost
            
        # limits on pwm below 
        min_pwm = 0 
        max_pwm = 64536
        iL = Vshunt/SHUNT_OHMS
        pwm_ref = saturate(65536-(int((vpot/3.3)*65536)),max_pwm,min_pwm) # convert the pot value to a PWM value for use later
        
        if iL < -1.9: # Limits for current to ensure components are not damaged
           
            duty = int(65536 -pwm_out) + 1000
            pwm.duty_u16(duty)
        if iL > 1.9:
            duty = int (65536- pwm_out) - 1000
            pwm.duty_u16(duty)
        
        if min_pwm < pwm_out < max_pwm:  # when code runs normally it should be within these bounds
            v_ref = BUS
            v_err = -vb + v_ref #ref voltage
            v_err_int = v_err_int + v_err 
            v_err_int = saturate(v_err_int, 10000, -10000)  # Saturate the integral error
            v_pi_out = (kp * v_err) + (ki * v_err_int) 
            diff = v_err-previous
            slide = saturate(50*v_err + 10*diff,30000,-30000) # Slide surface to help PI controller reach faster the desired value
            if v_err > 0.1:   # that means reference voltage is greater, so increase duty
                 v_pi_out = saturate(v_pi_out - slide,max_pwm,min_pwm)
            if v_err < -0.1: # that means reference voltage is smaller than vb , vb must decrease
                 v_pi_out = saturate(v_pi_out + slide,max_pwm,min_pwm)
       
            
            previous = v_err # stores current error for next iteration
            pwm_out = saturate(v_pi_out ,max_pwm,min_pwm)
            duty = int(65536-pwm_out) # invert as in skeleton code given on GitHub
            pwm.duty_u16(duty) # send the output of the PI controller out as PWM

        else:  # This is to set a pwm around halfway so that it can start tracking voltage correctly once again in case of a glitch
            v_err_int = 0
            pwm_out = 30000


        count = count + 1 # counter increases until 5 seconds are counted
        timer_elapsed = 0
        
        data = data + iL*vb*0.001 # every milisecond so energy will be power * 0.001 assuming is constant for intrval
        
        #  executes every 5 seconds to send to server net energy
        

        if count>4999:
            tosend = myclient('192.168.203.234', 5001) # create connection with the server
            tosend.senddata('Grid', str(data)) # send total energy to server
            tosend.close() # close communication with server
            data = 0
            print (vb) # used to check if the voltage is at desired bus, can be commented or ignored

                
            count = 0 #reset counter and start again
            
            
        






