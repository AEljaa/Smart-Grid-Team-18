from flask import Flask, jsonify , request
import requests
from flask_cors import CORS
import json

fname = "../db/deferable_db.json"  # our json database, if it doesn't exist, it gets made
last_three_sell_prices = []
grid_data={}
cap_data=""
cap_graph_data=[0]*60
profit=0
grid_graph_data=[0]*60
def cleanData(data):
    buyHist = []
    demandHist = []
    sellHist = []
    tick = []
    for item in data:
        buyHist.append(item['buy_price'])
        demandHist.append(item['demand'])
        sellHist.append(item['sell_price'])
        tick.append(item["tick"])
    return buyHist, demandHist, sellHist, tick
def cleanDef(data):
    dic={}
    for index, item in enumerate(data):
        dic[index] =[item['end'],item['energy'],item['start']]
    return dic
    
app = Flask(__name__)
CORS(app)  # This will prevent the annoying CORS errors we get whenever we access the server

def update_lag_array(new_price):
    global last_three_sell_prices 
    if (len(last_three_sell_prices)>=3):
        last_three_sell_prices.pop(0)
    last_three_sell_prices.append(new_price)

@app.route('/webdata', methods=['GET'])
def get_website_data():
    try:
        sun_response = requests.get('https://icelec50015.azurewebsites.net/sun')
        sun_data = sun_response.json()

        price_response = requests.get('https://icelec50015.azurewebsites.net/price')
        price_data = price_response.json()

        demand_response = requests.get('https://icelec50015.azurewebsites.net/demand')
        demand_data = demand_response.json()
        current_tick = price_data["tick"]
        return jsonify({
            'buy_price': price_data["buy_price"],
            'sell_price': price_data["sell_price"],
            'sun': sun_data["sun"],
            'demand': demand_data["demand"],
            'tick': price_data["tick"]
        })
    except Exception as e:
        print(f"Error fetching webs data: {e}")
        return jsonify({'error': 'An error occurred while fetching webs data'}), 500


@app.route('/yesterday', methods=['GET'])
def get_yesterday_data():
    try:
        response = requests.get('https://icelec50015.azurewebsites.net/yesterday')
        yesterday_data = response.json()
        buyHist, demandHist, sellHist, ticks = cleanData(yesterday_data)
        print(buyHist, demandHist, sellHist)
        print(ticks)
        return jsonify({
            'buyHist': buyHist,
            'demandHist': demandHist,
            'sellHist': sellHist,
            'tick': ticks
        })
    except Exception as e:
        print(f"Error fetching yesterday's data: {e}")
        return jsonify({'error': 'An error occurred while fetching yesterday data'}), 500

@app.route('/deferables', methods=['GET'])
def get_deferables_data():
    try:
        response = requests.get('https://icelec50015.azurewebsites.net/deferables')
        deferable_data = response.json()
        return jsonify(deferable_data)
    except Exception as e:
        print(f"Error fetching deferables data: {e}")
        return jsonify({'error': 'An error occurred while fetching deferables data'}), 500

@app.route('/curr_deferables', methods=['GET'])
def get_curr_deferables_data():
    try:
        with open(fname, 'r+b') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching deferables data: {e}")
        return jsonify({'error': 'An error occurred while fetching deferables data'}), 500

@app.route('/helper', methods=['GET'])
def send_helper_data():
    try:
        current_response = requests.get('https://icelec50015.azurewebsites.net/price')
        current_data = current_response.json()
        current_sell_price = current_data['sell_price']  
        tick= current_data['tick']
    

        demand_response = requests.get('https://icelec50015.azurewebsites.net/demand')
        demand_data=demand_response.json()

        sun_response = requests.get('https://icelec50015.azurewebsites.net/sun') # Send GET request to third party server
        sun_data = sun_response.json()['sun']

        deferable_response = requests.get('https://icelec50015.azurewebsites.net/deferables')
        deferable_data = deferable_response.json()

        deferable_data=cleanDef(deferable_data)
        update_lag_array(current_sell_price)

        # Ensure we have at least three values
        if len(last_three_sell_prices) < 3:
            return jsonify({'error': 'Not enough data for lag values'}), 500


        return jsonify({
            'current_sell_price': current_sell_price,
            'demand' : demand_data['demand'],
            'lags' : last_three_sell_prices,
            'tick': tick,
            'sun' : sun_data,
            'deferables' : deferable_data
        })
    except Exception as e:
        print(f"Error in helper: {e}")
        return jsonify({'error': 'An error occurred while processing helper'}), 500

@app.route('/send_grid_data', methods=['POST'])
def receive_grid_data():
    global grid_data
    try:
        received_data = request.json  # Data is sent in json format so got to handle
        grid_data = received_data
        response = requests.get('https://icelec50015.azurewebsites.net/price')
        tick = response.json()["tick"]
        grid_graph_data[tick]=grid_data
        grid_graph_data[tick+1:]=len(grid_graph_data[tick+1:])*[0]
 

        return jsonify({'message': 'Data received successfully'}), 200
    except Exception as e:
        print(f"Error processing received data: {e}")
        return jsonify({'error': 'An error occurred while processing data'}), 500

@app.route('/forward_grid_data', methods=['GET'])
def forward_grid_data():
    global profit
    try:
        # Check if data is stored
        response = requests.get('https://icelec50015.azurewebsites.net/price')
        buyprice = response.json()["buy_price"]
        sellprice = response.json()["sell_price"]
        print("In forward grid data sending", grid_data, "type is ", type(grid_data))
        if(int(grid_data)>0):
            profit -= abs(int(grid_data)*sellprice)
        if(int(grid_data)<0):
            profit +=abs(int(grid_data)*buyprice)
        if grid_data:
            print("Sending",grid_data)
            return jsonify({
                'profit': profit,
                'value' : grid_data

            })
        else:
            return jsonify({'message': 'No data available'}), 404
    except Exception as e:
        print(f"Error forwarding data: {e}")
        return jsonify({'error': 'An error occurred while forwarding data'}), 500

@app.route('/forward_grid_graph_data', methods=['GET'])
def forward_grid_graph_data():
    try:
        print(grid_graph_data)
        return jsonify(grid_graph_data), 200
    except Exception as e:
        print(f"Error forwarding data: {e}")
        return jsonify({'error': 'An error occurred while forwarding data'}), 500

@app.route('/send_cap_data', methods=['POST'])
def receive_cap_data():
    global cap_data
    global cap_graph_data
    try:
        response = requests.get('https://icelec50015.azurewebsites.net/price')
        tick = response.json()["tick"]
        received_data = request.json  # Data is sent in json format so got to handle   
        cap_data = received_data
        cap_graph_data[tick]=int(cap_data)
        cap_graph_data[tick+1:]=len(cap_graph_data[tick+1:])*[0]
        print(cap_graph_data)
        print('Received data:', cap_graph_data)
        return jsonify({'message': 'Data received successfully'}), 200
    except Exception as e:
        print(f"Error processing received data: {e}")
        return jsonify({'error': 'An error occurred while processing data'}), 500

@app.route('/forward_cap_data', methods=['GET'])
def forward_cap_data():
    try:
        # Check if data is stored
        if cap_data:
            print("In forward cap data sending", cap_data, "type is ", type(cap_data))
            return jsonify(cap_data), 200
        else:
            return jsonify({'message': 'No data available'}), 404
    except Exception as e:
        print(f"Error forwarding data: {e}")
        return jsonify({'error': 'An error occurred while forwarding data'}), 500

@app.route('/forward_cap_graph_data', methods=['GET'])
def forward_cap_graph_data():
    try:
        print(cap_graph_data)
        return jsonify(cap_graph_data), 200
    except Exception as e:
        print(f"Error forwarding data: {e}")
        return jsonify({'error': 'An error occurred while forwarding data'}), 500

if __name__ == '__main__':
    app.run(port=4000, debug=True)  # API hosted on http://127.0.0.1:4000
