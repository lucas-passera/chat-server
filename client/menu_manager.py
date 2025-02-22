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
       
    def check_password_hash(provided_password, stored_hash):
        
        if bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True
        else:
            return False
        

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

        print("\n----------------------------------\n")
        print("CHOOSE AN OPTION:")
        print()
        print("1-Chat.")
        print("2-Users.")
        print("3-Messages.")
        print("0-Exit.")
        print("\n----------------------------------\n")

#--------------------------------------------------------------------------------------------------------------------

    def show_menu_user_not_found(self):
        print("\n----------------------------------\n")
        print("1-Try again.")
        print("2-Enter with ID.")
        print("3-Create a new user.")
        print("0-Exit.")
        print("\n----------------------------------\n")

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