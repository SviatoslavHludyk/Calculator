import json
import os
import math
import datetime

USERS_FILE_PATH = 'users.json'
HISTORY_FILE_PATH = 'history.log'

logged_user = None

def register():
    with open(os.path.join(USERS_FILE_PATH), 'r') as f:
        user_data = json.load(f)
    while True:
        username = input("Enter a username: ")
        if username in user_data:
            print("Username already exists. Please try a different username.")
        else:
            break
    password = input("Enter a password: ")
    user_data[username] = {'password': password}
    with open(os.path.join(USERS_FILE_PATH), 'w+') as f:
        json.dump(user_data, f)
    print("Account created successfully.")    

def login():
    with open(os.path.join(USERS_FILE_PATH), 'r') as f:
        user_data = json.load(f)
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
    if password == user_data[username]['password']:
        print("Login successful!")
        return username
    else:
        print("Incorrect password. Please try again.")

def log_history(username, message):
    if os.path.isfile(HISTORY_FILE_PATH) == False or os.stat(HISTORY_FILE_PATH).st_size == 0:
        with open(os.path.join(HISTORY_FILE_PATH), 'a+') as file:
            file.write("date, username, message\n")
    now = datetime.datetime.now()
    new_log = str(now) + ", " + username + ", " + message + "\n"
    with open(os.path.join(HISTORY_FILE_PATH),'a+') as file:
        file.write(new_log)

def check_if_number_is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def calc_without_login(username):
    calculator = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }
    while True:
        x = input('Enter first number: ')
        if check_if_number_is_float(x):
            operation = input('Enter operation in {}: '.format(list(calculator.keys())))
            if operation in calculator.keys():
                y = input('Enter second number: ')
                if check_if_number_is_float(y):
                    x = float(x)
                    y = float(y)
                    try:
                        result = calculator[operation](x, y)
                        if username is not None:
                            message = str(x) + operation + str(y) + '=' + str(result)
                            log_history(username, message)
                        return result
                    except ZeroDivisionError:
                        print('Zero division error.')
                        return 'Zero division error.'
                else:
                    print('Invalid number. It must be float. Try again. ')
            else:
                print('Incorrect operation. Operation must be in {}'.format(list(calculator.keys())))
        else:
            print('Invalid number. It must be float. Try again. ')
    
def calc_with_login(username):
    calculator = {
        'sin': lambda x: math.sin(x),
        'cos': lambda x: math.cos(x),
        'tan': lambda x: math.tan(x),
        'cot': lambda x: math.tan(x)**(-1),
    }

    while True:
        operation = input('Enter operation between {}: '.format(list(calculator.keys())))
        if operation in calculator.keys():
            x = float(input('Enter number: '))
            if check_if_number_is_float(x):
                try:
                    result = calculator[operation](x)
                    message = operation + '(' + str(x) + ')' + '=' + str(result)
                    log_history(username, message)
                    return result
                except ZeroDivisionError:
                    print('Zero division error.')
                    return 'Zero division error.'
            else:
                print('Invalid number. It must be float. Try again. ')
        else:
            print('Incorrect operation. Operation must be in {}'.format(list(calculator.keys())))


try:
    with open(os.path.join(USERS_FILE_PATH), 'r') as f:
        user_data = json.load(f)
except Exception:
    with open(os.path.join(USERS_FILE_PATH), 'w') as f:
        user_data = {}
        json.dump(user_data, f)


while True:
    if os.stat(os.path.join(USERS_FILE_PATH)).st_size == 0:
        print("No users found. Please register a new account.")
        register()
    else:
        if logged_user is not None:
            print(f"You are currently logged in as: {logged_user}\n")
            options = ['Calculate arithmetic', 'Calculate trigonometric', 'Logout']
        else:
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
            print("Result: ", calc_without_login(logged_user))
        elif selected_option == 'Calculate trigonometric':
            print("Result: ", calc_with_login(logged_user))
        elif selected_option == 'Logout':
            user_data.clear()
            logged_user = None
            print("Logout successful!\n")
        elif selected_option == 'Quit':
            break
