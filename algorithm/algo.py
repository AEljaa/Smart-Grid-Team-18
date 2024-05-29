import requests,time
def naive_algorithm(price,yesterday_list):
    if(price < sum(yesterday_list)/len(yesterday_list)):
        print("BUY")
    else:
        print("SELL")

def algorithm(price, yesterday_list, demand): #Sophie's aproach - need to refine within quartiles 2 and 3 (currently do nothing)
    yesterday_list.sort()
    median = yesterday_list[len(yesterday_list) // 2]
    mean = sum(yesterday_list) / len(yesterday_list)
    q3_index = int(0.75 * len(yesterday_list))  # Convert float index to integer
    q3 = yesterday_list[q3_index]
    q1_index = len(yesterday_list) // 4
    q1 = yesterday_list[q1_index]
    print(f"median {median} mean {mean} q3 {q3} q1 {q1}")
    # Just now need to connec this to a socket and send the response and amount -- TODO
    if price < q1:
        print(f"BUY at {1+demand/4} multiplier at price {price}")
    elif price >q3:
        print(f"SELL at {1+demand/4} multiplier at price {price}")


url="http://127.0.0.1:4000/algorithm" #from our flask api
while True:
    source = requests.get(url).json()
    price=source['current_sell_price']
    yesterday_list=source['yesterday_sell_prices']
    demand=source['demand']
    algorithm(price,yesterday_list,demand)
    time.sleep(5)

    




