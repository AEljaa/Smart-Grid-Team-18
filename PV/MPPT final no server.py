from machine import Pin, I2C, ADC, PWM, Timer
import network
import time
import time
import socket

# Basic signals to control logic flow
global timer_elapsed
timer_elapsed = 0
count = 0
first_run = 1

# Need to know the shunt resistance
global SHUNT_OHMS
SHUNT_OHMS = 0.10

# saturation function for anything you want saturated within bounds
def saturate(signal, upper, lower): 
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
        
va_pin = ADC(Pin(28))
vb_pin = ADC(Pin(26))
# Set up the I2C for the INA219 chip for current sensing
ina_i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=2400000)

# Some PWM settings, pin number, frequency, duty cycle limits and start with the PWM outputting the default of the min value.
pwm = PWM(Pin(9))
pwm.freq(100000)
min_pwm=0
max_pwm = 40000
pwm_out = min_pwm




# main function, always executes
while True:
    if first_run:
        # for first run, set up the INA link and the loop timer settings
        ina = ina219(SHUNT_OHMS, 64, 5)
        ina.configure()
        first_run = 0
        # This starts a 1kHz timer which we use to control the execution of the control loops and sampling
        loop_timer = Timer(mode=Timer.PERIODIC, freq=5000, callback=tick)
        
        # Gains etc for the PID controller
        i_ref = 0 # Voltage reference for the CL modes
        i_err = 0 # Voltage error
        i_err_int = 0 # Voltage error integral
        i_pi_out = 0 # Output of the voltage PI controller
        ki = 50 # Boost Integral Gain
        step=0.0005#Step size for p&o
        prev_iin=0
        prev_pin=0
        isc=0
        imax=0
        im=0
    
    if timer_elapsed == 1: # This is executed at 5kHz
        va = 1.017*(12490/2490)*3.3*(va_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
        vb = 1.015*(12490/2490)*3.3*(vb_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
        Vshunt = ina.vshunt()
        
        iL = Vshunt/SHUNT_OHMS
        iin=iL
        vin=vb
        pin=vin*-iin
        #check if on right of MPP and move to left of MPP
        if (iin+1.03*vin) >= 4:
            im-=0.01
        #check if on left of MPP calc MPP
        else:
            isc=iin-0.02*vin 
            im=0.8972*isc+0.002 
        i_diff=im-iin
#       
        if abs(i_diff)>=0.005:
            kp=20
            #agressive references used for speed
            if iin<im:
                i_ref=1
            if iin>im:
                i_ref=-2
#       if close to MPP P &0
        else:
            kp=6
            i_ref=im
            if pin>prev_pin:
                if iin>prev_iin:
                    i_ref -=step
                else:
                    i_ref +=step
            elif pin<prev_pin:
                if iin<prev_iin:
                    i_ref -=step
                else:
                    i_ref +=step
            else:
                i_ref = i_ref
            i_ref=saturate(i_ref,-0.0001,-1) #keep reference within safe ranges
            
        prev_iin = iin
        prev_pin = pin
        
        
        i_err = i_ref-iL
        # calculate the error in voltage
        if min_pwm < pwm_out < max_pwm:    
            i_err_int = i_err_int + i_err # add it to the integral error
            i_err_int = saturate(i_err_int, 10000, -10000) # saturate the integral error
        i_pi_out = (kp*i_err)+(ki*i_err_int) # Calculate a PI controller output
        
        pwm_out = saturate(i_pi_out,max_pwm,min_pwm) # Saturate that PI output
        duty = int(65536-pwm_out)
        pwm.duty_u16(duty) # Send the output of the PI controller out as PWM
        # Keep a count of how many times we have executed and reset the timer so we can go back to waiting
        count += 1
        timer_elapsed = 0
        
        # This set of prints executes every 100 loops (every 0.2s)
        if count > 50:
            print((pin)) 
            count = 0