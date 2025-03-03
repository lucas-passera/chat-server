import bcrypt
from colorama import Fore
import requests

#url="http://184.72.171.214:8081/"
url="http://localhost:8081/"
class DisplayManager:

#------------------------ CONSTRUCTOR -------------------------------------------------------------------------------   

    def __init__(self):
        pass
        
#--------------------------------------------------------------------------------------------------------------------   

    def show_welcome(self):
        
        print()
        print(Fore.WHITE + "-------------------------------------------------------------------------------")
        print(Fore.LIGHTGREEN_EX + "                           ¡WELCOME TO CHAT-SERVER!     ")
        print(Fore.WHITE + "-------------------------------------------------------------------------------")
        print()

#--------------------------------------------------------------------------------------------------------------------

    def show_login_menu(self):
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

        