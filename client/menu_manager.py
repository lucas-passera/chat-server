import json
import sys
import bcrypt
import requests

url = "http://localhost:8081/"

class MenuManager :

    def __init__(self, client):
        self.client = client
    
#------------------------------------------- Menu methods ------------------------------------------------

    def show_app_menu_and_choose(self):
        while True:
            print("----------------------------------")
            print("Choose an option:")
            print()
            print("1-Chat.")
            print("2-Users.")
            print("3-Messages.")
            print("0-Exit.")
            print("----------------------------------")
            option = input("Enter your choice: ").strip()
            print()
            if option in {"0", "1", "2", "3"}:
                return int(option)
            else:
                print("Invalid option. Please enter 0, 1, 2, or 3.\n")
    
    def user_notfound_menu(self):  
        while True:
            print("USER NOT FOUND.")
            print("1-Try again.")
            print("2-Enter with ID.")
            print("3-Create a new user.")
            print("0-Exit.")
            option = input("Choose an option: ").strip()
            print()

            if option == "0":
                return 0  

            elif option =="1":
                self.username = MenuManager.request_username(self) 
            elif option == "2":
                user_id = MenuManager.request_id(self)
                return user_id
            
            elif option == "3":
                username = input("Please enter your username: ")
                print(f"New username: {username}")
                
                while True:
                    password = input("Please enter your password (max 15 characters): ")
                    if not password:
                        print("Password cannot be empty. Please try again.")
                    elif len(password) > 15:
                        print("Password is too long. Maximum length is 15 characters.")
                    else:
                        data = {"username": username, "password": password}
                        break 
                response = requests.post(url + "users/", json=data)                
                
                if response.status_code == 200: 
                    response_data = response.json()  
                    user_id = response_data["user"].get("ID")  
                    print(f"User created successfully with ID: {user_id}")
                    print()
                    break

                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    response_data=response.json() 
                    user_id=response_data.get("id")

                return user_id
              
            
            else:
                print("\nInvalid option.") 

    def request_id(self):
        while True:
            id= input("\nEnter your user ID:")
            print()
            if 0 < len(id) <= 5 and id.isdigit():
                return id
            else:
                print("Invalid ID. The user ID must be between 1 and 5 digits long. Only numbers are allowed.")

    def request_username(self):
        while True:
            username = input("\nEnter your username:")
            print()
            if 0 < len(username) <= 15 :
                return username
            else:
                print("Invalid username. The username must be between 1 and 15 characters")

    def request_pass(self):
        while True:
            password = input("Please enter your password (0 para salir): ")
            if (password=="0"):
                return password    
            else:
                if not password:
                    print("Password cannot be empty. Please try again.")
                elif len(password) > 15:
                    print("Password is too long. Maximum length is 15 characters.")
                else:
                    return password
                
                
    def choice_function(self, a: int,client):
        print(f"You selected option {a}.")
        if a == 1:
            print("Starting chat...")
            print()
            print("**********************************")
            print("Use ./menu to return to the menu.")
            print("**********************************")
            print()
            client.start_chat()
            sys.exit()

        elif a == 2:
            print("Showing users...")
            response = requests.get(f"{url}users/") 
            formatted_response = json.dumps(response.json(), indent=4)
            print(formatted_response)

        elif a == 3:
            print("Showing messages...")
            response = requests.get(f"{url}messages/") 
            formatted_response = json.dumps(response.json(), indent=4)
            print(formatted_response)

        elif a == 0:
            print("Exiting...")
            sys.exit()

    
    def check_password_hash(provided_password, stored_hash):
        if bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True
        else:
            return False