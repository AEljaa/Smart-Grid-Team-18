#import RPi.GPIO as GPIO  ##comment out for server: its pi only
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
        try: 
            while not self.stop:
                print("Connecting to",self.host,self.port)
                self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.mySocket.connect((self.host,self.port))        
                
                self.mydataout = str(self.myid)
                self.mySocket.send(self.mydataout.encode())
                print("Sent:",self.mydataout)
                
                self.mydatain = self.mySocket.recv(1024).decode()
                print("Received:",self.mydatain)
                
                if self.mydataout == self.mydatain:
                    print("Data recieved ok")
                else:
                    print("Data error")
                           
                self.mySocket.close()
                print("Disconnected from",self.host,self.port)
                
        except KeyboardInterrupt:
                print("Quitting")
                stop = True

        except:
                print("Error")
                
        finally:
                print("Cleaning")
                #GPIO.cleanup()
                #give the server some time
                time.sleep(1)

class myserver():

    def __init__(self,host,port):
        
        self.host = host
        self.port = port
        self.stop = False
        self.powerlist=[1,0.5,3,4]

        self.mydatain = ""
        self.mydataout = ""
    
        print("Creating server...")
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.mySocket.bind((self.host,self.port))
        #so it always listenis
        while not self.stop:

            try:
                self.mySocket.listen(1)
                self.conn, self.addr = self.mySocket.accept()
                print("Connection from:", str(self.addr[0]))
                
                self.mydatain = self.conn.recv(1024).decode()
                print("Received:", str(self.mydatain))
                self.mydataout = str(self.mydatain).upper()
                self.conn.send(self.mydataout.encode())
                print("Sent:", str(self.mydataout))
                if str(self.mydataout) == "LED1" or str(self.mydataout) == "LED2" or str(self.mydataout) == "LED3" or str(self.mydataout) == "LED4":
                    self.mydataout = getnewdemanddata()
                self.conn.send(self.mydataout.encode())
                print("Sent:", str(self.mydataout))
                self.conn.close()
                print("Disconnected:",str(self.addr[0]))

               
                
            except KeyboardInterrupt:
                print("Quitting")
                stop = True

        self.mySocket.close()
 
if __name__ == "__main__":
    #we just need to comment out which one we want it to run 
    #and put in the right ip adresses
    #sender = threading.Thread(target=myclient, args=('10.10.1.138',5000), daemon=True).start()
    
        receiver = threading.Thread(target=myserver, args=('146.169.219.119',5001), daemon=True).start()

        
