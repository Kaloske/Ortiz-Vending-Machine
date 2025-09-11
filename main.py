balance = 100

stockDict = {
    'apple': 10,
    'banana': 10,
}

PriceDict = {
    'apple': 20,
    'banana': 25,
}

def check_price(key): #returns the price if given the item name
    if key in PriceDict:
        return PriceDict[key]
    return None

def check_stock(key): #returns the stock if given the item name
    if key in stockDict:
        return stockDict[key]
    return None

def sell_item(item, quantity):
    if check_stock(item) and check_price(item): #checks if present in  both the price and stock dictionary
        global balance
        balance -= check_price(item)
        stockDict[item] -= quantity


def output_list():
    print(f"Balance: {balance}$")
    for i, (item, stock) in enumerate(stockDict.items(), start=1):
        price = check_price(item)
        print(f"[{i}] {item.title()}: x{stock} {price}$ ")

output_list()
sell_item('banana', 1)
output_list()

