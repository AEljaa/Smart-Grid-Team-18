import time
import socket
import threading
import helper
import json
import requests
class MyServer:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stop = False
        self.powerlist = [1, 0.5, 3, 4]
        self.currentengmade = 2
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySocket.bind((self.host, self.port))
        print("Creating server...")

    def handle_client(self, conn, addr):
        try:
            print("Connection from:", str(addr))
            while True:
                self.mydatain = conn.recv(1024).decode()
                if not self.mydatain:
                    break
                print("Received:", str(self.mydatain))
                self.mydataout = str(self.mydatain).upper()
                conn.send(self.mydataout.encode())
                print("Sent:", str(self.mydataout))

                if self.mydatain in ["LED1", "LED2", "LED3", "LED4"]:
                    self.mydataout = str(helper.return_demand()+",")
                    conn.send(self.mydataout.encode())
                    print("Sent:", str(self.mydataout))
                elif self.mydatain == "Grid":
                    algoout = helper.main()
                    self.mydataout = json.dumps(algoout)
                    conn.send(self.mydataout.encode())
                    print("Sent:", str(self.mydataout))
                    self.mydataout = str(helper.return_demand())
                    conn.send(self.mydataout.encode())
                    print("Sent:", str(self.mydataout))
                elif self.mydatain == "Storage":
                    algoout = helper.main()
                    algoout_parsed = json.loads(algoout)
                    instruction = algoout_parsed.get("instruction")
                    ratio = algoout_parsed.get("ratio")
                    demand = helper.return_demand()
                    if instruction == "BUY":
                        amount = ratio * demand
                    else:
                        amount = ratio * demand * -1
                    self.mydataout = str(self.currentengmade + amount - demand)
                    conn.send(self.mydataout.encode())
                    print("Sent:", str(self.mydataout))
                elif self.mydatain == "PV":
                    self.currentengmade = float(conn.recv(1024).decode())
                else:
                    self.mydataout = "sorry, you are not recognized"
                    conn.send(self.mydataout.encode())
                    print("Sent:", str(self.mydataout))
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
#Send Grud data to flask endpoint flask then sends to our website
def send_data_to_flask(data):
    try:
        url = 'http://localhost:4000/send_data'  
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print('Data sent successfully to Flask backend')
        else:
            print(f'Failed to send data. Status code: {response.status_code}')
    except Exception as e:
        print(f"Error sending data to Flask backend: {e}")

if __name__ == "__main__":
    server = MyServer('0.0.0.0', 5001)
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
  #  data={
  #      "Generated" : 100,
  #      "Stored" : 33
  #          }
  #  
  #  send_data_to_flask(data)
  #  
    # Keep the main thread running to catch keyboard interrupts
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.stop = True
        server_thread.join()
