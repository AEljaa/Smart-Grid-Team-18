
from machine import Pin, I2C, ADC, PWM, Timer
import network
import time
import socket
import math

class myclient():

    def __init__(self,host,port):
        
        self.host = host
        self.port = port
        #self.count = 0
        self.stop = False
        self.mydataout = "please work"
        self.mydatain = ""
        self.buy=0
        self.sell=0
        
        try: 
            #while not self.stop:
                print("Connecting to",self.host,self.port)
                self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                self.mySocket.connect((self.host,self.port))        

                

                
        except KeyboardInterrupt:
                print("Quitting")
                stop = True
                self.mySocket.close()

        except:
                print("Error")
                self.mySocket.close()
                
        finally:
                print("Cleaning")
                #self.mySocket.close()
                print("get ehere")
                #GPIO.cleanup()
                #give the server some time
                time.sleep(1)
    def senddata(self,datatosend):
        self.mydataout=datatosend
        self.mySocket.send(self.mydataout.encode())
        print("Sent:",self.mydataout)
                
        self.mydatain = self.mySocket.recv(1024).decode()
        print("Received:",self.mydatain)
                
        if self.mydataout.upper() == self.mydatain:
            print("Data recieved ok")
            self.mydatain = self.mySocket.recv(1024).decode()
            self.sell=self.mydatain
            self.mydatain = self.mySocket.recv(1024).decode()
            self.buy=self.mydatain
            
            print("Received:",self.mydatain)
        else:
            print("Data error")
    def retrivesent(self):
        return self.mydatain
    def close(self):
        print("closing")
        self.mySocket.close()
        
previous = 0
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

ks = 12 # Slide constant
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
kp = 20 # Boost Proportional Gain tuned
ki = 10 # Boost Integral Gain tuned
BUS = 7

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

SSID = 'Sophie'
PASSWORD = 'EEE123EEE'
def connectwifi (ssid, password):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid,password) #connects to given SSID

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
        #ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x01\x9F') # PG = 1
        #ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x09\x9F') # PG = /2
        ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x19\x9F') # PG = /8
        ina_i2c.writeto_mem(conf.address, conf.REG_CALIBRATION, b'\x00\x00')

connectwifi(SSID,PASSWORD)
# Here we go, main function, always executes
#tosend = myclient('146.169.240.74',5001)  # object to send data

for i in range(0,1000000): # should be the while true loop
    try:
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
            CL = OL_CL_pin.value() # Are we in closed or open loop mode
            BU = BU_BO_pin.value() # Are we in buck or boost mode?
                
            # New min and max PWM limits and we use the measured current directly
            min_pwm = 0 
            max_pwm = 64536
            iL = Vshunt/SHUNT_OHMS
            pwm_ref = saturate(65536-(int((vpot/3.3)*65536)),max_pwm,min_pwm) # convert the pot value to a PWM value for use later
            #tosend = myclient('146.169.253.108',5001)  # object to send data
            if iL < -1.5:
               
                duty = int(65536 -pwm_out) + 1000
                pwm.duty_u16(duty)
            if iL > 1.5:
                duty = int (65536- pwm_out) - 1000
                pwm.duty_u16(duty)
            
            if min_pwm < pwm_out < max_pwm:  # maybe greater or equal
                v_ref = BUS
                v_err = -vb + v_ref #ref voltage
                v_err_int = v_err_int + v_err 
                v_err_int = saturate(v_err_int, 10000, -10000)  # Saturate the integral error
                v_pi_out = (kp * v_err) + (ki * v_err_int) #+ (ks * v_err if vb>BUS+0.5) - ks * (v_err if vb<BUS-0.5)
                diff = v_err-previous
                slide = 20*v_err+10*diff
                if slide > 0.1:   # that means reference voltage is greater, so increase duty
                     v_pi_out = v_pi_out - slide
                if slide < -0.1: # that means reference voltage is smaller than vb , vb must decrease
                     v_pi_out = v_pi_out + slide
           
                
                previous = v_err  
                pwm_out = saturate(v_pi_out ,max_pwm,min_pwm)
                duty = int(65536-pwm_out) # Invert because reasons
                pwm.duty_u16(duty) # Send the output of the PI controller out as PWM
                #tosend.senddata("Power imported: "+ str(iL*va) if iL>=0 else "Power exported:"+ str(iL*vb))
                #tosend.close()
            else:
                v_err_int = 0
                pwm_out = 30000


            count = count + 1
            timer_elapsed = 0
            # current tracking idea for changing duty cycle to keep v constant and current minimal
            
            # This set of prints executes every 100 loops by default and can be used to output debug or extra info over USB enable or disable lines as needed
            if (i%100)==0:

                
                print(vb) # to see if it does indeed work as it should
                count = 0

    except:
                print("error")




