import json
import os
import math
import datetime

# Define the file path where the user data will be stored
USERS_FILE_PATH = 'users.json'
HISTORY_FILE_PATH = 'history.json'

logged_user = None
clear = lambda: os.system('clear')


try:
    # Load existing user data from the JSON file
    with open(os.path.join(USERS_FILE_PATH), 'r') as f:
        user_data = json.load(f)
except Exception:
    # If the file doesn't exist, create it and initialize an empty dictionary
    with open(os.path.join(USERS_FILE_PATH), 'w') as f:
        user_data = {}
        json.dump(user_data, f)

def register():
    """Allows the user to register a new account."""
    while True:
        username = input("Enter a username: ")
        if username in user_data:
            print("Username already exists. Please try a different username.")
        else:
            break
    password = input("Enter a password: ")
    # Add the new user to the user data dictionary
    user_data[username] = {'password': password}
    # Save the updated user data to the JSON file
    with open(os.path.join(USERS_FILE_PATH), 'w+') as f:
        json.dump(user_data, f)
    print("Account created successfully.")    

def login():
    """Allows the user to log in to an existing account."""
    while True:
        username = input("Enter your username: ")
        if username in user_data:
            break
        else:
            print("Invalid username.")
            choice = input("Do you want to register a new account? (y/n): ")
            if choice.lower() == 'y':
                register()
            else:
                return

    password = input("Enter your password: ")
    # Check if the provided password matches the stored password for the given username
    if password == user_data[username]['password']:
        print("Login successful!")
        return username
    else:
        print("Incorrect password. Please try again.")

def log_history(username, message):
    """Allows the logged in user to save calc history."""


def calc_without_login(*username):
    x = int(input('Enter first number: '))
    operation = input('Enter operation: ')
    y = int(input('Enter second number: '))
    calculator = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }
    if operation in calculator.keys():
        result = calculator[operation](x, y)
        if username != None:
            message = str(x) + operation + str(y) + '=' + str(result)
            log_history (username, message)
        return result
    
def calc_with_login(username):
    operation = input('Enter operation: ')
    x = int(input('Enter number: '))
    calculator = {
        'sin': lambda x: math.sin(x),
        'cos': lambda x: math.cos(x),
        'tan': lambda x: math.tan(x),
        'cot': lambda x: math.tan(x)**(-1),
    }
    if operation in calculator.keys():
        result = calculator[operation](x)
        message = operation + '(' + str(x) + ')' + '=' + str(result)
        log_history (username, message)
        return result
    
# Main program loop
while True:
    if os.stat(os.path.join(USERS_FILE_PATH)).st_size == 0:
        print("No users found. Please register a new account.")
        register()
    else:
        if logged_user != None:
            # logged_in_username = next(iter(user_data))
            print(f"You are currently logged in as: {logged_user}\n")
            options = ['Calculate arithmetic', 'Calculate trigonometric', 'Logout']
        else:
            # No user is currently logged in
            options = ['Calculate arithmetic', 'Register', 'Login']

        options.append('Quit')

        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")

        choice = input("\nEnter your choice: ")

        try:
            choice = int(choice)
            selected_option = options[choice-1]
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
            continue

        if selected_option == 'Register':
            register()
        elif selected_option == 'Login':
            logged_user = login()
        elif selected_option == 'Calculate arithmetic':
            clear()
            print("Result: ", calc_without_login(logged_user))
        elif selected_option == 'Calculate trigonometric':
            clear()
            print("Result: ", calc_with_login(logged_user))                              
        elif selected_option == 'Logout':
            # Clear the user data to log out the current user
            user_data.clear()
            logged_user = None
            print("Logout successful!\n")
        elif selected_option == 'Quit':
            break
