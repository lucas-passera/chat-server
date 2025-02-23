import json
import sys
import bcrypt
from colorama import Fore
import requests

url = "http://localhost:8081/"

class MenuManager :

#------------------------ CONSTRUCTOR -------------------------------------------------------------------------------   

    def __init__(self, client):
        self.client = client
        
#--------------------------------------------------------------------------------------------------------------------   

    def welcome(self):
        
        print()
        print(Fore.WHITE + "-------------------------------------------------------------------------------")
        print(Fore.LIGHTGREEN_EX + "                           ¡WELCOME TO CHAT-SERVER!     ")
        print(Fore.WHITE + "-------------------------------------------------------------------------------")
        print()
#--------------------------------------------------------------------------------------------------------------------

    def show_menu_user_not_login(self):
        print("-------------------------------------------------------------------------------\n")
        print(f"{Fore.LIGHTGREEN_EX}1{Fore.RESET}-Enter with Username.")
        print(f"{Fore.LIGHTGREEN_EX}2{Fore.RESET}-Enter with ID.")
        print(f"{Fore.LIGHTGREEN_EX}3{Fore.RESET}-Create a new user.")
        print(f"{Fore.LIGHTGREEN_EX}0{Fore.RESET}-Exit.")
        print("\n-------------------------------------------------------------------------------\n")

#-------------------------------------------------------------------------------------------------------------------- 

    def show_main_menu(self):

        print(Fore.WHITE + "-------------------------------------------------------------------------------\n")
        print(f"{Fore.LIGHTGREEN_EX}1{Fore.RESET}-Chat.")
        print(f"{Fore.LIGHTGREEN_EX}2{Fore.RESET}-Users.")
        print(f"{Fore.LIGHTGREEN_EX}3{Fore.RESET}-Messages.")
        print(f"{Fore.LIGHTGREEN_EX}0{Fore.RESET}-Exit.")
        print(Fore.WHITE + "\n-------------------------------------------------------------------------------")
      

#--------------------------------------------------------------------------------------------------------------------   

    def show_start_chat(self):
        
        print()
        print(Fore.LIGHTYELLOW_EX+"*******************************************************************************************"+Fore.RESET)
        print("-------------------------- USE "+Fore.LIGHTYELLOW_EX+"./MENU"+Fore.RESET+" TO RETURN TO MAIN MENU ------------------------------")
        print(Fore.LIGHTYELLOW_EX+"*******************************************************************************************"+Fore.RESET)
        print(Fore.LIGHTGREEN_EX+ "Starting chat..."+Fore.RESET)
        
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

    def show_starting_chat(self):

        print("Starting chat...")
        print()
        print("*********************************")
        print("Use ./menu to return to the menu.")
        print("*********************************")
        print()

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