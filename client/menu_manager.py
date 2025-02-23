import json
import sys
import bcrypt
from colorama import Fore
import requests

url="http://184.72.171.214:8081/"

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
        print("\n\n\n\n\n\n")
        print(Fore.LIGHTYELLOW_EX+"*******************************************************************************************"+Fore.RESET)
        print("-------------------------- USE "+Fore.LIGHTYELLOW_EX+"./MENU"+Fore.RESET+" TO RETURN TO MAIN MENU ------------------------------")
        print(Fore.LIGHTYELLOW_EX+"*******************************************************************************************"+Fore.RESET)
        print()
        print(Fore.LIGHTYELLOW_EX+ "Starting chat..."+Fore.RESET)
                      
        
#--------------------------------------------------------------------------------------------------------------------
       
    def check_password_hash(provided_password, stored_hash):
        
        if bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True
        else:
            return False

#--------------------------------------------------------------------------------------------------------------------        

    def check_username(self, username):

        #url = f"http://localhost:8081/users/check-username/{username}"  LOCAL
        url = f"{url}users/check-username/{username}"  # EC2
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Username is "+Fore.LIGHTGREEN_EX+"available"+Fore.RESET)
                return True
            elif response.status_code == 409:
                print(Fore.LIGHTRED_EX+"Username already exists. "+Fore.RESET+"\n")
                return False
            else:
                print(f"{Fore.LIGHTRED_EX}Error:{Fore.RESET} {response.status_code}, Could not check username")
                return False
        except requests.exceptions.RequestException as e:
            print(f"{Fore.LIGHTRED_EX}Error connecting to server:{Fore.RESET} {e}")
            return False
        
#--------------------------------------------------------------------------------------------------------------------
