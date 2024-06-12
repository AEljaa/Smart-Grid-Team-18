import asyncio
import websockets
import json
async def handler(websocket, path):
    data={
        "Generated" : "lolGen",
        "Stored" : "lolstored"
            }
    sendjson=json.dumps(data)
    await websocket.send(sendjson)

if __name__ == "__main__":
    #we just need to comment out which one we want it to run 
    #and put in the right ip adresses
    #sender = threading.Thread(target=myclient, args=('10.10.1.138',5000), daemon=True).start()

    #receiver = threading.Thread(target=myserver, args=('146.169.253.108z',5001), daemon=True).start()
    #Communication from data server to backend webserver
    start_server = websockets.serve(handler, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()        
