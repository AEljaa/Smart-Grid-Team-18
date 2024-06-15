import time
import socket
import threading
import helper
import json
import requests
def send_cap_data_to_flask(data):
    try:
        url = 'http://localhost:4000/send_cap_data'  
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print('Data sent successfully to Flask backend')
        else:
            print(f'Failed to send data. Status code: {response.status_code}')
    except Exception as e:
        print(f"Error sending data to Flask backend: {e}")
def send_grid_data_to_flask(data):
    try:
        url = 'http://localhost:4000/send_grid_data'  
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print('Data sent successfully to Flask backend')
        else:
            print(f'Failed to send data. Status code: {response.status_code}')
    except Exception as e:
        print(f"Error sending data to Flask backend: {e}")

class MyServer:

    def __init__(self, host, port):
        self.host = host
        self.powerimported=0
        self.poweroutported=0
        self.port = port
        self.stop = False
        self.powerlist = [1, 0.5, 3, 4]
        self.currentengmade = 2
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySocket.bind((self.host, self.port))
        print("Creating server...")

    def handle_client(self, conn, addr): ### Whyyy so many self.var, just do var. Why so many str()?
        try:
            print("Connection from:", str(addr))
            while True:
                self.mydatain = conn.recv(1024).decode()
                if not self.mydatain:
                    break
                print("Received:", str(self.mydatain))
                self.mydataout = str(self.mydatain).upper()
                conn.send(self.mydataout.encode()) ## ??? Try to make send/receive ping-pong. send-receive-send-receive, this is redundant send which can complicate a subsequent send
                print("Sent:", str(self.mydataout))

                if self.mydatain in ["LED1", "LED2", "LED3", "LED4"]:
                    currentdemand= int(helper.return_demand())
                    playroom=4-int(currentdemand)
                    self.mydataout=helper.deferablehell(playroom)#tick, deferable list need added
                    print(int(self.mydataout))
                    conn.send(str(self.mydataout).encode())
                    print("Sent LED:", float(self.mydataout))

                elif self.mydatain == "Grid":
                    self.mydatain = conn.recv(1024).decode()
                    #FIND WHAT MEAN KIN MONEY TERMS AND GO ON WEB
                    ## if power positive then you are buying if negative then selling expect in joules
                    send_grid_data_to_flask(self.mydatain)
                    print("Received from Grid:", str(self.mydatain))
                    conn.send(str("GRID").encode())

                elif self.mydatain == "Storage":
                    self.mydatain = conn.recv(1024).decode()
                    print("Revieved from Storage:", str(self.mydatain))
                    send_cap_data_to_flask(self.mydatain)
                    if self.mydatain!="0": #if we have no enge
                        algoout=helper.algorithm(46- float(self.mydatain))
                        self.mydataout=str(algoout)
                        conn.send(str(self.mydataout).encode())
                        print("Sent Storage:", str(self.mydataout))
                    else:
                        self.mydataout=str(0)
                        conn.send(self.mydataout.encode())
                        print("Sent Storage:", str(self.mydataout))

                elif self.mydatain == "PV":
                    self.currentengmade = float(conn.recv(1024).decode())
                    print(self.currentengmade)
                    self.mydataout = str(helper.return_irradiance())
                    conn.send(self.mydataout.encode())
                    print("Sent PV:", str(self.mydataout))


                else:
                    self.mydataout = "sorry, you are not recognized"
                    conn.send(self.mydataout.encode())
                    print("Sent PV:", str(self.mydataout))
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()
            print("Disconnected:", str(addr))

    def start(self):
        self.mySocket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        while not self.stop:
            try:
                conn, addr = self.mySocket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                print("Quitting")
                self.stop = True
            except Exception as e:
                print("Error:", e)

        self.mySocket.close()

if __name__ == "__main__":
    server = MyServer('192.168.43.86', 5001)
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    # Keep the main thread running to catch keyboard interrupts
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.stop = True
        server_thread.join()
