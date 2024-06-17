from machine import Pin, I2C, ADC, PWM
from PID import PID

import network
import time

import time
import socket
import threading




class myclient():

    def __init__(self,host,port):
        
        self.host = host
        self.port = port
        self.count = 0
        self.stop = False
        self.mydataout = ""
        self.mydatain = ""
        self.psetpoint= 0
        self.success = 0
        try: 
            #while not self.stop:
                print("Connecting to",self.host,self.port)
                print("1")
                self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("2")
                self.mySocket.connect((self.host,self.port))
                self.success = 1
                print("4")
        except KeyboardInterrupt:
                print("Quitting")
                stop = True
                self.mySocket.close()

        except:
                print("Error")
                self.mySocket.close()
                
        finally:
                print("Cleaning")
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
            ##extra reciver
            self.mydatain = self.mySocket.recv(1024).decode()
            print("Received:",self.mydatain)

            self.psetpoint=self.mydatain
        else:
            print("Data error")
    def close(self):
        print("closing")
        self.mySocket.close()
        
                
                
#WIFI Connection
SSID = 'Sophie'
PASSWORD = 'EEE123EEE'
def connectwifi (ssid, password):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid,password)
    ip=wlan.ifconfig()[0]
    print(ip)
    



connectwifi(SSID,PASSWORD)






vret_pin = ADC(Pin(26))
vout_pin = ADC(Pin(28))
vin_pin = ADC(Pin(27))
pwm = PWM(Pin(0))
pwm.freq(100000)
pwm_en = Pin(1, Pin.OUT)

pid = PID(0.02, 5, 0, setpoint=0.3, scale='ms')


Psetpoint = 0.5
count = 0
pwm_out = 0
pwm_ref = 0
setpoint = 0.0
delta = 0.05

attempt = True
failcount = 0

def saturate(duty):
    if duty > 62500:
        duty = 62500
    if duty < 100:
        duty = 100
    return duty

while attempt:
    pwm_en.value(1)

    vin = 1.026*(12490/2490)*3.3*(vin_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
    vout = 1.026*(12490/2490)*3.3*(vout_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
    vret = 1*3.3*((vret_pin.read_u16()-350)/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
    count = count + 1
    Pout = vout*setpoint
    
    
    pwm_ref = pid(vret)
    pwm_ref = int(pwm_ref*65536)
    pwm_out = saturate(pwm_ref)
    pwm.duty_u16(pwm_out)
    
    if count > 2000:
        
        """sender = threading.Thread(target=myclient, args=('146.169.240.74',5001))
        sender.daemon=False
        sender.start()"""
        #Server IP
        try:
            if failcount < 100:
                #server IP in quotes
                sender=myclient('146.169.252.111',5001)
                sender.senddata(str("LED4"))
                sender.close()
            
                if Psetpoint != sender.psetpoint:
                    Psetpoint = sender.psetpoint
                    print("Received:",Psetpoint)
                
                Power = float(Psetpoint) 
            else:
                Power = 1.5
                
            print("Vin = {:.3f}".format(vin))
            print("Vout = {:.3f}".format(vout))
            print("Vret = {:.3f}".format(vret))
            print("Duty = {:.0f}".format(pwm_out))
            print("setpoint = {:.3f}".format(float(setpoint)))
            print("Psetpoint = {:.3f}".format(Power))
            count = 0
              
            if Power > 4:
                setpoint = 1/vout
                
            elif Power <= 3:
                setpoint = 0
                
            else:
                setpoint = (Power-3)/vout
                
            pid.setpoint = setpoint
            
            if sender.success == 1:
                faicount = 0
            
            
    
        except:
            print("Connection Failed")
            failcount =+ 1
                
                
        finally:
            sender.close()




