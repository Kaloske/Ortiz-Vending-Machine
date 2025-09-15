running = True
balance = 1000


class InventoryItem:
    def __init__(self, name, stock, price):
        self.name = name
        self.price = price
        self.stock = stock

    def sell(self, quantity):
        global balance
        if quantity <= self.stock:
            if quantity * self.price <= balance:
                self.stock -= quantity
                balance -= quantity * self.price
                return None
            else:
                return output_error("Balance Error")
        else:
            return output_error('Stock insufficient')

    def __str__(self):
        return f'Inventory Item: {self.name} {self.stock} {self.price}'


chips = InventoryItem('chips', 10, 20)
chocolate = InventoryItem('chocolate', 10, 25)
coca_cola = InventoryItem('coca cola', 10, 30)

inventory = [chips, chocolate, coca_cola]
inventory_dict = {item.name: item for item in inventory}

def output_error(message):  # I separated this so that I have the other functions focusing on just returning
    print(f"Error! {message}")

def check_index_range(index_number):  # used to check if a number is in the dictionary's index range
    if 0 <= index_number < len(inventory):
        return True
    elif index_number > len(inventory):
        output_error(f"Item Index:{index_number + 1} not found in the inventory.")
        return False
    return None

def output_list():  # prints inventory and stuff
    print(f"Balance: {balance}$")
    for i, item in enumerate(inventory, start=1):
        print(f"[{i}] {item.name.title()}: {item.price}$ x{item.stock}")

def help_screen():
    print("""
    To buy an item you may:
    1. Type its displayed index number or name.
    2. Use the buy command. (buy, name/index number, quantity) or (buy, name/index number)
        Ex. buy, apple, 2
        Ex. buy, 2, 1
        Ex. buy, 1
        Ex. buy, banana

    Typing 'inventory' will display the inventory.

    Typing 'exit' will exit the program.
    
    When prompted with a confirmation screen, you may answer with y/yes or n/no
    """)

def confirm_input(prompt):  # takes a prompt and returns true if the user answers y and vice versa, supports yes/no
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

def ask_for_quantity(item): #given inventory object will askk for the quantity
    while True:  # loops until a number is inputted
        quantity = (input_handler(f"Input desired quantity for '{item.name}'\n> ")[0])
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

def buy_from_index(item_index, quantity=0):
    try:
        quantity = int(quantity)
        item_index = int(item_index) - 1
        if quantity >= 0:
            if check_index_range(item_index): #check if it's in the range
                item = list(inventory_dict.values())[item_index]
                if quantity == 0:
                    quantity = ask_for_quantity(item)
                if confirm_input(f"Would you like to buy {quantity} '{item.name} for {item.price * quantity}$'? [y/n]"):
                    item.sell(quantity)
            elif item_index < 0:
                output_error("Item index cannot be negative or zero.")
        else:
            output_error("Quantity cannot be zero.")
    except ValueError:
        output_error(f"Quantity must be a valid integer.")

def buy_from_name(item, quantity=0):
    try:
        quantity = int(quantity)
        if item in list(inventory_dict.keys()):
            item = inventory_dict[item]
            if quantity == 0: quantity = ask_for_quantity(item) #final check for quantity
            elif quantity < 0:
                output_error("Quantity cannot be negative")
                return
            if confirm_input(f"Would you like to buy {quantity} '{item.name} for {item.price * quantity}$'? [y/n]"):
                item.sell(quantity)
        else:
            output_error(f"'{item}' not found in the inventory.")
    except ValueError:
        output_error(f"Quantity must be a valid integer.")

def process_input(user_input):
    match user_input:
        case ["inventory"]:
            output_list()
        case ["help"]:
            help_screen()
        case ["exit"]:
            global running
            if confirm_input(f"Are you sure you want to exit the program? [y/n]"):
                running = False
        case ["buy", item, quantity]:
            if item[1:].isdecimal() or item.isdecimal():
                buy_from_index(item, quantity)
            else:
                buy_from_name(item, quantity)
        case ["buy", item] | [item]:
            if item[1:].isdecimal() or item.isdecimal():
                buy_from_index(item)
            else:
                buy_from_name(item)
        case _:
            output_error("Invalid input.")
def main():
    print("Nishie's Vending Machine! v.1.3 \nType 'help' for instructions.")
    while running:
        output_list()
        process_input(input_handler("> "))

main()
