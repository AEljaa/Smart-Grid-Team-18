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
        response = requests.post(url, headers=headers, json=float(data))
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
        response = requests.post(url, headers=headers, json=float(data))
        if response.status_code == 200:
            print('Data sent successfully to Flask backend')
        else:
            print(f'Failed to send data. Status code: {response.status_code}')
    except Exception as e:
        print(f"Error sending data to Flask backend: {e}")

class MyServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stop = False
        self.currentengmade = 2
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySocket.bind((self.host, self.port))
        print("Creating server...")

    def handle_client(self, conn, addr):
        try:
            print("Connection from:", str(addr))
            while True:
                data_in = conn.recv(1024).decode()
                if not data_in:
                    break
                print("Received:", data_in)

                if data_in in ["LED1", "LED2", "LED3", "LED4"]:
                    try:
                        data_out = helper.greedyDeferable()
                        print(f"greedyDeferable() returned: {data_out}")
                        conn.send(str(data_out).encode())
                        print("Sent LED:", data_out)
                    except Exception as e:
                        print(f"Error processing LED command: {e}")
                        conn.send("ERROR".encode())

                elif data_in == "Grid":
                    data_in = conn.recv(1024).decode()
                    send_grid_data_to_flask(data_in)
                    print("Received from Grid:", data_in)
                    conn.send("GRID".encode())

                elif data_in == "Storage":
                    data_in = conn.recv(1024).decode()
                    print("Received from Storage:", data_in)
                    send_cap_data_to_flask(data_in)
                    if data_in != "0":
                        algo_out = helper.energyAlgorithm(46 - float(data_in))
                        conn.send(str(algo_out).encode())
                        print("Sent Storage:", algo_out)
                    else:
                        conn.send("0".encode())
                        print("Sent Storage: 0")

                elif data_in == "PV":
                    self.currentengmade = float(conn.recv(1024).decode())
                    data_out = str(helper.return_irradiance())
                    conn.send(data_out.encode())
                    print("Sent PV:", data_out)

                else:
                    data_out = "sorry, you are not recognized"
                    conn.send(data_out.encode())
                    print("Sent:", data_out)
        except Exception as e:
            print("Error
