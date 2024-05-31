from flask import Flask, jsonify
import requests
from flask_cors import CORS

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

app = Flask(__name__)
CORS(app)  # This will prevent the annoying CORS errors we get whenever we access the server

@app.route('/sun', methods=['GET'])  
def get_sun_data():
    try:
        response = requests.get('https://icelec50015.azurewebsites.net/sun') # Send GET request to third party server
        sun_data = response.json()
        return jsonify(sun_data)
    except Exception as e:
        print(f"Error fetching sun data: {e}")
        return jsonify({'error': 'An error occurred while fetching sun data'}), 500

@app.route('/price', methods=['GET'])
def get_price_data():
    try:
        response = requests.get('https://icelec50015.azurewebsites.net/price')
        price_data = response.json()
        return jsonify(price_data)
    except Exception as e:
        print(f"Error fetching price data: {e}")
        return jsonify({'error': 'An error occurred while fetching price data'}), 500

@app.route('/demand', methods=['GET'])
def get_demand_data():
    try:
        response = requests.get('https://icelec50015.azurewebsites.net/demand')
        demand_data = response.json()
        return jsonify(demand_data)
    except Exception as e:
        print(f"Error fetching demand data: {e}")
        return jsonify({'error': 'An error occurred while fetching demand data'}), 500

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

@app.route('/helper', methods=['GET'])
def send_helper_data():
    try:
        current_response = requests.get('https://icelec50015.azurewebsites.net/price')
        current_data = current_response.json()
        current_sell_price = current_data['sell_price']  
    
        yesterday_response = requests.get('https://icelec50015.azurewebsites.net/yesterday')
        yesterday_data = yesterday_response.json()
        _, _, yesterday_sell_prices, _ = cleanData(yesterday_data)

        demand_response = requests.get('https://icelec50015.azurewebsites.net/demand')
        demand_data=demand_response.json()

        return jsonify({
            'current_sell_price': current_sell_price,
            'yesterday_sell_prices': yesterday_sell_prices,
            'demand' : demand_data['demand']
        })
    except Exception as e:
        print(f"Error in helper: {e}")
        return jsonify({'error': 'An error occurred while processing helper'}), 500

if __name__ == '__main__':
    app.run(port=4000, debug=True)  # API hosted on http://127.0.0.1:4000
