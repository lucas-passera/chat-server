import json
import sys
import bcrypt
import requests

url = "http://localhost:8081/"

class MenuManager :

#------------------------ CONSTRUCTOR -------------------------------------------------------------------------------   

    def __init__(self, client):
        self.client = client
    
#--------------------------------------------------------------------------------------------------------------------   
    
    def user_notfound_menu(self): 

        invalidOpt=0 #
        option = 2  #value for enter 

        while True:

            if(option==2):

                if(invalidOpt==0):
                    print("ERROR: USER NOT FOUND.\n")

                self.show_menu_user_not_found()
                option = input("Choose an option: ").strip()
                print()

                if option == "0":
                    print("Exiting...")
                    return 0  

                elif option == "1":
                    invalidOpt = 0 
                    self.username = MenuManager.request_username(self)
                    response = requests.get(f"{url}users/username/{self.username}")

                    while True:
                        if response.status_code == 200:
                            user_data = response.json()

                            self.user_id = user_data.get("user", {}).get("ID") 
                            self.username = user_data.get("user", {}).get("username") 
                            self.password = user_data.get("user", {}).get("password") 

                            in_password = MenuManager.request_pass(self)
                            if in_password == "0":
                                sys.exit()

                            if MenuManager.check_password_hash(in_password, self.password):
                                print("¡SUCCESSFUL REGISTRATION!")
                                self.register_ok = 1
                                return self.register_ok  # ✅ Retornar el valor actualizado
                            else:
                                print("Incorrect password, please, try again!.")

                        else:
                            return self.user_notfound_menu()

                elif option == "2":

                    invalidOpt=0 
                    self.user_id = MenuManager.request_id(self)

                    while True:

                        response = requests.get(f"{url}users/{self.user_id}")

                        if response.status_code == 200:

                            user_data = response.json() 
                            self.user_id = user_data.get("user", {}).get("ID")
                            self.username = user_data.get("user", {}).get("username") 
                            self.password = user_data.get("user", {}).get("password") 

                            while True:

                                in_password = MenuManager.request_pass(self)

                                if (in_password=="0"):
                                    self.register_ok=0
                                    return self.register_ok
                                      

                                if MenuManager.check_password_hash(in_password, self.password):
                                    print("¡SUCCESSFUL REGISTRATION!")
                                    self.register_ok = 1
                                    print("----------------------------------")
                                    print(f"¡Hi, {self.username}!")
                                    option=1
                                    return self.register_ok
                                else:
                                    print("Incorrect password, please, try again.")

                            break              

                        else:
                            MenuManager.user_notfound_menu(self)
                            break
                    break 

                elif option == "3":

                    invalidOpt=0 
                    username = self.get_valid_username()
                    print(f"Your chosen username is: {username}")

                    while True:
                        password = input("Please enter your password: ")

                        if not password:
                            print("Password cannot be empty. Please try again.")
                        elif password=="0":
                            print("Password cannot be 0")
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
                        self.register_ok=1
                        print()
                        break

                    else:

                        print(f"Error: {response.status_code} - {response.text}")
                        response_data=response.json() 
                        user_id=response_data.get("id") 
                        self.register_ok=0
                        sys.exit()
                    return user_id, self.register_ok
                
                else:
                    invalidOpt=1
                    option=2
                    print("Invalid option.\n") 

#--------------------------------------------------------------------------------------------------------------------   

    def show_app_menu_and_choose(self):

        while True:

            self.show_main_menu()
            option = input("Enter your choice: ").strip()
            print()

            if option in {"0", "1", "2", "3"}:
                return int(option)
            else:
                print("Invalid option. Please enter 0, 1, 2, or 3.\n")

#--------------------------------------------------------------------------------------------------------------------   

    def request_id(self):

        while True:
            id= input("\nEnter your user ID:")
            print()

            if 0 < len(id) <= 5 and id.isdigit():
                return id
            else:
                print("Invalid ID. The user ID must be between 1 and 5 digits long. Only numbers are allowed.")

#--------------------------------------------------------------------------------------------------------------------   

    def request_username(self):

        while True:
            username = input("Enter your username:")
            print()

            if 0 < len(username) <= 15 :
                return username
            else:
                print("Invalid username. The username must be between 1 and 15 characters")
                
#--------------------------------------------------------------------------------------------------------------------   

    def request_pass(self):

        while True:
            password = input("Please enter your password o 0 para salir: ")

            if (password=="0"):
                return password  
              
            else:
                if not password:
                    print("Password cannot be empty. Please try again.")
                elif len(password) > 15:
                    print("Password is too long. Maximum length is 15 characters.")
                else:
                    return password
                
#--------------------------------------------------------------------------------------------------------------------  
                 
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

#--------------------------------------------------------------------------------------------------------------------
       
    def check_password_hash(provided_password, stored_hash):
        
        if bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True
        else:
            return False
        
#-------------------------------------------------------------------------------------------------------------------- 
      
    def handle_chat_menu(self, url, ws):

        while True:

            selected_option = self.show_app_menu_and_choose()
            print(f"You selected option {selected_option}.")
            print()

            if selected_option == 1:

                self.show_starting_chat()
                break

            elif selected_option == 2:

                print("Showing users...")
                print()
                response = requests.get(f"{url}users/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()

            elif selected_option == 3:

                print("Showing messages...")
                print()
                response = requests.get(f"{url}messages/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()

            elif selected_option == 0:

                print("Exiting...")
                print()
                ws.close() 
                return             

#--------------------------------------------------------------------------------------------------------------------   

    def welcome(self):
        
        print()
        print("----------------------------------")
        print("---- ¡Welcome to chat-server! ----")
        print("----------------------------------")
        print()

#--------------------------------------------------------------------------------------------------------------------  

    def show_starting_chat(self):

        print("Starting chat...")
        print()
        print("*********************************")
        print("Use ./menu to return to the menu.")
        print("*********************************")
        print()

#-------------------------------------------------------------------------------------------------------------------- 

    def show_main_menu(self):

        print("----------------------------------\n")
        print("CHOOSE AN OPTION:")
        print()
        print("1-Chat.")
        print("2-Users.")
        print("3-Messages.")
        print("0-Exit.")
        print("\n----------------------------------\n")

#--------------------------------------------------------------------------------------------------------------------

    def show_menu_user_not_found(self):

        print("1-Try again.")
        print("2-Enter with ID.")
        print("3-Create a new user.")
        print("0-Exit.\n")
        print("----------------------------------\n")

#--------------------------------------------------------------------------------------------------------------------

    def check_username(self, username):

        url = f"http://localhost:8081/users/check-username/{username}"  # Cambia el puerto si es necesario
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Username is available")
                return True
            elif response.status_code == 409:
                print("Username already exists. Please choose another one.")
                return False
            else:
                print(f"Error: {response.status_code}, Could not check username")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to server: {e}")
            return False
        
#--------------------------------------------------------------------------------------------------------------------

    def get_valid_username(self):
        while True:
            username = input("Please enter your username: ")
            if self.check_username(username):
                return username
            else:
                print("Try again with a different username.")