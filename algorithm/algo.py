import requests
import json

url="http://127.0.0.1:4000/algorithm" #from our flask api

def naive_algorithm(price,yesterday_list):
    if(price < sum(yesterday_list)/len(yesterday_list)):
        print("BUY")
    else:
        print("SELL")

def algorithm(price, yesterday_list, demand): #Sophie's aproach - need to refine within quartiles 2 and 3 (currently do nothing)
    yesterday_list.sort()
    instruction=""
    ratio=0
    q3_index = int(0.75 * len(yesterday_list))  # Convert float index to integer
    q3 = yesterday_list[q3_index]
    q1_index = len(yesterday_list) // 4
    q1 = yesterday_list[q1_index]
    if price < q1:
        instruction="BUY"
        ratio=1+demand/4
    elif price >q3:
        instruction="SELL"
        ratio=1+demand/4
    value= {
        "instruction" : instruction,
        "ratio" : ratio
    }

    return json.dumps(value)

def main():
    source = requests.get(url).json()
    price=source['current_sell_price']
    yesterday_list=source['yesterday_sell_prices']
    demand=source['demand']
    return algorithm(price,yesterday_list,demand)

    




