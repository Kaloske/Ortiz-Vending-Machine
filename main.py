from unittest import case

from unicodedata import digit

#to do: Add more error messages, add support for selecting via index number, etc...

running = True
balance = 1000

class InventoryItem:
    def __init__(self, name, stock, price):
        self.name = name
        self.price = price
        self.stock = stock

    def sell(self, quantity):
        global balance
        if quantity >= self.stock:
            if quantity * self.price <= balance:
                self.stock -= quantity
                balance -= quantity * self.price
                return None
            else:
                return output_error("Balance Error")
        else:
            return output_error('Inventory is out of stock')

    def __str__(self):
        return f'Inventory Item: {self.name} {self.stock} {self.price}'

chips = InventoryItem('Apple', 10, 20)
chocolate = InventoryItem('Banana', 10, 25)

inventory = [chips, chocolate]

stockDict = {
    'apple': 10,
    'banana': 10,
    'coca cola': 10,
}

priceDict = {
    'apple': 20,
    'banana': 25,
    'coca cola': 5,
}

def get_price(key): #returns the price if given the item name
    if key in priceDict:
        return priceDict.get(key)
    return None

def get_key(key): #returns the stock if given the item name
    if key in stockDict:
        return priceDict.get(key)
    return None

def get_item_from_index(item_index): #assumes that
    if item_index < len(stockDict):
        return list(stockDict.keys())[item_index]
    return None

def sell_item(item, quantity):
    global balance
    print(item)
    quantity = int(quantity)
    if get_key(item) and get_price(item):
        stock = stockDict[item]
        price = priceDict[item]
        if price*quantity <= balance:
            if 0 < quantity <= stock:
                balance -= get_price(item) * quantity
                stockDict[item] = stockDict[item] - quantity
                print(stockDict[item])
            else: output_error("Insufficient stock")
        else:output_error(f"Balance Insufficient.")
    else: output_error(f"'{item}' not found in the inventory.")

def output_error(message): #I separated this so that I have the other functions focusing on just returning
    print(f"Error! {message}")

def check_index_range(index_number): #used to check if a number is in the dictionary's index range
    if 0 <= index_number < len(stockDict):
        return True
    elif index_number > len(stockDict):
        output_error(f"Item Index:{index_number+1} not found in the inventory.")
        return False
    return None

def output_list(): #prints inventory and stuff
    print(f"Balance: {balance}$")
    for i, (item, stock) in enumerate(stockDict.items(), start=1):
        price = get_price(item)
        print(f"[{i}] {item.title()}: {price}$ x{stock}")

def help_screen():
    print("""
    To buy an item you may:
    1. Type its displayed index number or name.
    2. Use the buy command. (buy, name/index number, quantity) or (buy, name/index number)
        Ex. buy apple 2
        Ex. buy 2 1
        Ex. buy 1
        Ex. buy banana
        
    Typing 'inventory' will display the inventory.
    
    Typing 'exit' will exit the program.
    """)

def confirm_input(prompt): #takes a prompt and returns true if the user answers y and vice versa, supports yes/no
    while True:
        print(prompt)
        userinput = input("> ").lower().split()
        match userinput:
            case ["y"] | ["yes"]:
                return True
            case ["n"] | ["no"]:
                return False
            case _:
                print("Invalid input")

def buy_command(item, quantity): #take only string name
    #buy given the item name and quantity
    try:
        quantity = int(quantity)
        if item and quantity > 0:
            quantity = int(quantity)
            if confirm_input(f"You would like to purchase {quantity} {item} for {quantity * get_price(item)}$, y/n?"):
                sell_item(item, quantity)
        elif quantity <= 0:
            output_error("Quantity cannot be negative or zero.")
        return None
    except ValueError:
        output_error(f"Quantity must be an integer.")

def ask_for_quantity(item):
    while True:  # loops until a number is inputted
        quantity = (input_handler(f"Input desired quantity for '{item}'\n> ")[0])
        try:
            quantity = int(quantity)
            if quantity > 0:
                return quantity
            elif quantity <= 0:
                output_error("Quantity cannot be negative or zero.")
        except ValueError:
            output_error(f"Quantity must be an integer.")

def input_handler(prompt):
    return input(prompt).lower().split(", ")

def process_input(user_input):
    print(user_input)#processes commands and calls whatever function should be called
    match user_input:
        case ["inventory"]:
            output_list()
        case ["help"]:
            help_screen()
        case ["exit"]:
            global running
            running = False
        case ["buy", item, quantity]:
            try: #try treating the item as an index number
                item_index = int(item)-1
                if check_index_range(item_index):
                    item = get_item_from_index(item_index)
                    buy_command(item, quantity)
                elif item_index <= 0:
                    output_error("Item index cannot be negative or zero.")
            except ValueError: #it's not an index number so use it as the name instead
                if item in list(stockDict.keys()):
                    buy_command(item, quantity)
                else: output_error(f"'{item}' not found in the inventory.")
        case ["buy", item_index] | [item_index]:
            try:
                item_index = int(item_index)-1
                if check_index_range(item_index):
                    item = get_item_from_index(item_index)
                    buy_command(item, ask_for_quantity(item))
                elif item_index <= 0:
                    output_error("Item index cannot be negative or zero.")
            except ValueError:
                item = item_index
                if item in list(stockDict.keys()):
                    buy_command(item, ask_for_quantity(item))
                else:
                    output_error(f"'{item}' not found in the inventory.")
        case _:
            output_error("Invalid input.")

def main():
    print("Nishie's Vending Machine! v.1.0 \nType 'help' for instructions.")
    while running:
        output_list()
        process_input(input_handler("> "))
main()
