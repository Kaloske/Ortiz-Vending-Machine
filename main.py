class System: #using a class for system is much cleaner
    def __init__(self, balance, running):
        self.balance = balance
        self.running = running
    def deposit(self, amount):
        if amount.isdigit():
            amount = int(amount)
            self.balance += amount
        else:
            output_error("Please deposit a positive integer")
    def shutdown(self):
        self.running = False

class InventoryItem:
    def __init__(self, name, stock, price):
        self.name = name
        self.price = price
        self.stock = stock

    def sell(self, quantity): #this is all obvious, no need for comments
        if quantity > self.stock:
            return output_error('Stock insufficient')
        if self.price > system.balance:
            return output_error("Balance insufficient")
        self.stock -= quantity
        system.balance -= quantity * self.price
        return None

    def __str__(self):
        return f'Inventory Item: {self.name} {self.stock} {self.price}'

system = System(500, True)
chips = InventoryItem('chips', 10, 20)
chocolate = InventoryItem('chocolate', 10, 25)
coca_cola = InventoryItem('coca cola', 10, 30)
apple = InventoryItem('apple', 10, 30)

inventory = [chips, chocolate, coca_cola, apple]
inventory_dict = {item.name: item for item in inventory}

def output_error(message):  # I separated this so that I have the other functions focusing on just returning
    print(f"Error: {message}")

def valid_digit(number): #check if a string is actually a number
    try:
        int(number)
        return True
    except ValueError:
        return False

def check_index_range(index_number):  # used to check if a number is in the dictionary's index range
    if 0 <= index_number < len(inventory):
        return True
    elif index_number > len(inventory) or index_number < 0:
        return False
    return None

def output_list():  # prints inventory and stuff
    print(f"Balance: {system.balance}$")
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
    
    Typing add, (quantity) will deposit money to your balance
    
    When prompted with a confirmation screen, you may answer with y/yes or n/no
    """)

def input_handler(prompt): #gets input and returns it as a normalized list of words
    return input(prompt).lower().split(", ")

def confirm_input(prompt):  # takes a prompt and returns true if the user answers y and vice versa, supports yes/no
    while True:
        print(prompt)
        userinput = input_handler("> ")
        match userinput:
            case ["y"] | ["yes"]:
                return True
            case ["n"] | ["no"]:
                return False
            case _:
                print("Invalid input")

def ask_for_quantity(item): #given inventory object will ask for the quantity
    while True:  # loops until a number is inputted
        quantity = (input_handler(f"Input desired quantity for '{item.name}'\n> ")[0])
        if quantity.isdigit():
            quantity = int(quantity)
            if quantity > 0:
                return quantity
            elif quantity <= 0:
                output_error("Quantity cannot be negative or zero.")
        else:
            output_error(f"Quantity must be a valid positive integer.")

def buy_from_index(item_index, quantity=0):
    item_index = int(item_index) - 1
    if not check_index_range(item_index): #check if it's in the range
        output_error("Item index not found")
        return
    if not valid_digit(quantity): #check if we can actually make it an integer
        output_error(f"Quantity must be a valid positive integer.")
        return
    #basic checks passed! let's reassign them to the proper values
    quantity = int(quantity)
    item = list(inventory_dict.values())[item_index]
    if quantity < 0: #check if negative
        output_error("Quantity cannot be negative.")
        return
    if quantity == 0: #final check for quantity, if 0 ask for a quantity
        quantity = ask_for_quantity(item)
    if confirm_input(f"Would you like to buy {quantity} '{item.name} for {item.price * quantity}$'? [y/n]"):
        #All checks passed!
        item.sell(quantity)

def buy_from_name(item, quantity=0):
    if item not in list(inventory_dict.keys()): #check if in the inventory
        output_error(f"'{item}' not found in the inventory.")
        return
    if not valid_digit(quantity): #check if we can actually make it an integer
        output_error(f"Quantity must be a valid positive integer.")
        return
    # basic checks passed! let's reassign them to the proper values
    quantity = int(quantity)
    item = inventory_dict[item]
    if quantity < 0: #check if it's negative
        output_error("Quantity cannot be negative")
        return
    if quantity == 0:
        quantity = ask_for_quantity(item) #final check for quantity
    if confirm_input(f"Would you like to buy {quantity} '{item.name} for {item.price * quantity}$'? [y/n]"):
        # All checks passed!
        item.sell(quantity)

def process_input(user_input):
    match user_input:
        case ["inventory"]:
            output_list()
        case ["help"]:
            help_screen()
        case ["exit"]:
            if confirm_input(f"Are you sure you want to exit the program? [y/n]"):
                system.shutdown()
        case ["buy", item, quantity]:
            if valid_digit(item):
                buy_from_index(item, quantity)
            else:
                buy_from_name(item, quantity)
        case ["buy", item] | [item]:
            if valid_digit(item):
                buy_from_index(item)
            else:
                buy_from_name(item)
        case ["add", quantity]:
            system.deposit(quantity)
        case _:
            output_error("Invalid input.")

def main():
    print("Nishie's Vending Machine! v.1.5 \nType 'help' for instructions.")
    while system.running:
        output_list()
        process_input(input_handler("> "))
main()
