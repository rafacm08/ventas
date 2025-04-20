# Author: Rafael Cabello Martínez
# Name: ventas.py
# Date: 2025-03-27
# Version: 1.0
"""
Program to manage sales, commissions, and notifications.

This program allows store employees to add sold products to the
sales list and calculate the commission they will be paid for the
total number of products sold.
Additionally, the program allows the administrator to access
read, write, and add data commands to the invoices.txt file.
A message is also sent through the ntfy.sh API to notify the
administrator about profits and commissions.
"""
import urllib.request

sales = []

def read_file():
    """
    Reads the content of a file.

    This function allows opening the invoices.txt document.
    The function reads the content of the file and prints it to the console.
    Finally, the function closes the file.
    """
    with open("invoices.txt", "r", encoding="utf-8") as file:
        print(file.read())

def write_file():
    """
    The function overwrites the file.

    This function allows opening the invoices.txt document.
    The function overwrites the content of the file with a blank.
    Finally, the function closes the file.
    """
    with open("invoices.txt", "w", encoding="utf-8") as file:
        file.write("")

def add_to_file(info):
    """
    Adds content to the file.

    This function allows opening the invoices.txt document.
    The function adds content to the file.
    Finally, the function closes the file.
    """
    with open("invoices.txt", "a", encoding="utf-8") as file:
        file.write("\n" + info)

def greet_admin():
    """
    Allows access to commands.

    This function allows the administrator to access the read,
    write, and add data commands to the invoices.txt file,
    as long as the correct password is verified.
    """
    user_password = int(input("Write your password: "))

    if user_password == 12345:
        print("Welcome Rafa!")
        command = str(input("Write the command you want to execute:\nr-read file"
            "\nw-delete record"
            "\na-add data to the record\n"
            )).lower()
        if command == "r":
            read_file()
        elif command == "w":
            write_file()
            print("All changes have been saved")
        elif command == "a":
            add_to_file(str(input("What would you like to add? ")))
            print("All changes have been saved")
        else:
            print(f"Error: \"{command}\" is not a valid command.")
    else:
        print("Error: Incorrect password.")

def send_message(text):
    """
    Sends messages with data to the admin.

    This function allows sending a message through the ntfy.sh API
    to notify the administrator about profits and commissions.
    """
    data = str(text)\
    .encode('utf-8')
    req = urllib.request.\
        Request("https://ntfy.sh/rafa_1234_demo",  # Use your own link.
        data = data,
        method='POST' )
    with urllib.request.urlopen(req) as r:
        r.read().decode('utf-8')

def profit():
    """
    Calculates the company's profit.

    This function allows calculating the total profit of the company
    from the data stored in the invoices.txt file.
    """
    with open("invoices.txt", "r", encoding="utf-8") as file:
        elements = file.read().split()
        number_of_elements = len(elements)
        profit_index = 8
        paid_index = 2
        total_amount = 0
        times = int(number_of_elements/10)
        while times > 0:
            times -= 1
            total_amount += float(elements[profit_index])
            total_amount -= float(elements[paid_index])
            profit_index += 10
            paid_index += 10
    send_message(f"The company currently has {round(total_amount,2)} euros in its funds")

def cycle():
    """
    Exits or stays in the program.

    This function allows the user to choose between exiting
    or continuing with the program.
    """
    proceed = input("\nWrite exit for exit or continue for stay.\n").lower()
    if proceed == "exit":
        print("Thank you for using the program")
        input("Press enter to exit...")
    elif proceed == "continue":
        manage_input()
    else:
        print("Error: Invalid command")
        input("Press enter to exit...\n")

def process_employee(user_name):
    """
    Calculates the commission for the product list.

    This function allows store employees to add sold products to the
    sales list and calculate the commission they will be paid for the
    total number of products sold.
    """
    sales.clear()
    print(f"Hi {user_name}!")
    product_number = int(float(input("How many products would " \
    "you like to add to the sales list? ")))
    if product_number <= 0:
        raise ValueError
    while product_number > 0:
        product_number -= 1
        product_cost = float(input("Cost of the product sold($): "))
        if product_cost <= 0:
            raise ValueError
        sales.append(product_cost)

    commission = round(sum(sales)*13/100,2)
    print(f"Well done, you have collected {round(sum(sales),2)}$")
    print(f"You have earned {commission}$ in commission\nGreat job!\n")

    add_to_file(
        f"\n {user_name} received {commission} euros in "
        f"commission for collecting {round(sum(sales),2)} dolars"
    )
    send_message(
        f"{user_name} recived {commission}$ in commission "
        f"for collecting {round(sum(sales),2)}$"
    )
    profit()

    print("Registered in the file")

def validate_name(user_name):
    """This function allows verifying if the entered name is correct."""
    if len(str(user_name).split()) != 1:
        raise NameError
    return user_name

def manage_input():
    """
    This function validates the employee's name.

    The function checks if the entered name is correct.
    It also verifies if the name "admin" has been entered.
    And it allows managing possible errors.
    """
    try:
        user_name = input("What is your name? ")
        user_name = validate_name(user_name)
        if user_name == "admin":
            greet_admin()
        else:
            process_employee(user_name)

    except ValueError:
        print("Please enter a valid number\n")

    except FileNotFoundError:
        print("The file has not been created yet...")
        write_file()
        print("Creating file...")
        print("The file has been created successfully...")

    except NameError:
        print("Enter a single word...")

    except TypeError:
        print("Ups... Something went wrong")

    finally:
        cycle()

print("\n###############################")
print("Program - Calculate Commissions")
print("###############################\n\n")
manage_input()
