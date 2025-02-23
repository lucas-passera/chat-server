import json
import sys
import bcrypt
from colorama import Fore
import requests

url = "http://localhost:8081/"

class StateMachine:

#--------------------------------------------------------------------------------------------------------------------    

    def __init__(self, client):
        self.client = client
        self.status_update = {
            "status": "NOT-LOGIN-MENU",
            "text": f"Enter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the login menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"
            }

#--------------------------------------------------------------------------------------------------------------------

    def run(self):
        while self.status_update["status"] != "EXIT":
            print(self.status_update["text"])  
            input_user = input("> ").strip()
            print()
            self.processInput(input_user)
        print(Fore.LIGHTGREEN_EX+"Exiting..."+Fore.RESET)
        sys.exit()

#--------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------- 
       
    def processInput(self, input_user):

        status = self.status_update["status"]

#--------Status Divisor--------

        if status == "NOT-LOGIN-MENU":

            if input_user=="y" or input_user == "Y":

                self.client.menu_manager.show_menu_user_not_login()
                self.status_update = {"status": "SELECT_OPC-NOT_LOGIN_MENU", "text": f"Select an {Fore.LIGHTGREEN_EX}OPTION{Fore.RESET}:"}

            else:
                self.status_update = {"status": "EXIT", "text": "Exiting..."}  

#--------Status Divisor--------

        elif status == "SELECT_OPC-NOT_LOGIN_MENU":

            if input_user == "1":
                self.status_update = {"status": "ENTER_WITH_USERNAME", "text": "Enter your " + Fore.LIGHTGREEN_EX + "USERNAME" + Fore.RESET + ":"}

            elif input_user == "2":

                self.status_update = {
                    "status": "ENTER_WITH_ID",    
                    "text": "\nEnter your " + Fore.LIGHTGREEN_EX + "USER ID" + Fore.RESET + " or " +
                        Fore.LIGHTGREEN_EX + "0" + Fore.RESET +
                        " to cancel:"
                    }
                
            elif input_user == "3":
                self.status_update = {"status": "CREATE_USER", "text": "Enter a "+Fore.LIGHTGREEN_EX+"NEW USERNAME"+Fore.RESET+":"}

            elif input_user == "0":
                self.status_update = {"status": "EXIT", "text": "Saliendo del sistema..."}

            else:
                print (f"{Fore.LIGHTRED_EX + 'INVALID OPTION' + Fore.RESET}. Try again.\n")

#--------Status Divisor--------

        elif status == "ENTER_WITH_USERNAME":
            #validator
            while True:
                if 0 < len(input_user) <= 15 :
                    break
                else:
                    input_user = input(Fore.LIGHTRED_EX + "Invalid username. The username must be between 1 and 15 characters.\n"+Fore.RESET+"Try again:\n")

            response = requests.get(f"{url}users/username/{input_user}")

            if response.status_code == 200:
                
                print("Response Status:", Fore.LIGHTGREEN_EX + str(response.status_code)+" OK\n" + Fore.RESET)

                user_data = response.json()["user"]    # recibo el json del server
                self.client.user_data = {  #guardo solo lo que me interesa aca
                    "user_id": user_data.get("ID"),
                    "username": user_data.get("username"),
                    "password": user_data.get("password")
                }

                self.client.user_id = user_data.get("ID")  # Sincronizamos
                self.client.username = user_data.get("username")
                self.status_update = {
                    "status": "LOGIN_REQUEST_PASS",
                    "text": "Enter your password:"
                }

                print("User found:\n" + Fore.CYAN + f"ID: {self.client.user_data.get('user_id')}, Username: {self.client.user_data.get('username')}\n")

            else:

                if response.status_code == 404:
                    print("Response Status:", Fore.LIGHTRED_EX + str(response.status_code) + Fore.RESET)
                    self.status_update = {
                        "status": "NOT-LOGIN-MENU",
                        "text": f"{Fore.LIGHTRED_EX + 'USER NOT FOUND.' + Fore.RESET} \n\nEnter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the program menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"
                    }
                     
                elif response.status_code == 400: 

                    print("Response Status:", Fore.LIGHTRED_EX + str(response.status_code) +" BAD REQUEST "+ Fore.RESET)
                    self.status_update = {
                        "status": "NOT-LOGIN-MENU",
                        "text": f"\nEnter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the login menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"
                        }
                    
                else:

                    print("Response Status:", Fore.LIGHTRED_EX + str(response.status_code) + Fore.RESET)

                    self.status_update = {
                        "status": "NOT-LOGIN-MENU",
                        "text": f"\nEnter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the login menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"  
                    }

#--------Status Divisor--------

        elif status == "LOGIN_REQUEST_PASS":

            if input_user == "0":
                print("Exiting...")
                self.status_update = {"status": "EXIT", "text": "Saliendo..."}

            elif self.client.menu_manager.checkpasswordhash(input_user.encode(), self.client.user_data["password"].encode()):

                self.status_update = {
                        "status": "MAIN",
                        "text": f"{Fore.LIGHTGREEN_EX + '¡Registration completed successfully!' + Fore.RESET}. \n\nEnter any char to continue:"
                    }
                
            else:
                print(Fore.LIGHTRED_EX + "Incorrect password." + Fore.RESET + "\nPlease try again or enter ("+Fore.LIGHTGREEN_EX+ "0" +Fore.RESET+") to exit.")

#--------Status Divisor--------

        elif status == "ENTER_WITH_ID":

            try:

                input_user = int(input_user)  # Convertir a entero

                if input_user == 0:

                    self.status_update = {
                        "status": "NOT-LOGIN-MENU",
                        "text": f"Canceling... press ({Fore.LIGHTGREEN_EX}Y{Fore.RESET}) to return to the registration menu or ({Fore.LIGHTGREEN_EX}ANY KEY{Fore.RESET}) to exit."
                        }
                    
                elif 0 < input_user < 10000:  # [0 < ID USER < 9999]

                    response = requests.get(f"{url}users/{input_user}")

                    if response.status_code == 200:

                        print("Response Status:", Fore.LIGHTGREEN_EX + str(response.status_code) + " OK" + Fore.RESET)

                        user_data = response.json()["user"]    # recibo el json del server

                        self.client.user_data = {  #guardo solo lo que me interesa aca
                            "user_id": user_data.get("ID"),
                            "username": user_data.get("username"),
                            "password": user_data.get("password")
                        }

                        self.client.user_id = user_data.get("ID")  # Sincronizamos
                        self.client.username = user_data.get("username")
                        self.status_update = {
                            "status": "LOGIN_REQUEST_PASS",
                            "text": "Enter your password:"
                        }

                        print("User found:\n" + Fore.CYAN + f"ID: {self.client.user_data.get('user_id')}, Username: {self.client.user_data.get('username')}\n")

                    else:

                        self.status_update = {
                            "status": "NOT-LOGIN-MENU",
                            "text": f"User not found, press ({Fore.LIGHTGREEN_EX}Y{Fore.RESET}) to return to the registration menu or ({Fore.LIGHTGREEN_EX}ANY KEY{Fore.RESET}) to exit."
                        }

                else:
                    print(Fore.LIGHTRED_EX + "INVALID ID." + Fore.RESET + " (ID MUST BE IN THIS RANGE: 0<ID<10000).\nTry again. ")

            except ValueError:  # Maneja el caso en que input_user no sea un número

                print(Fore.LIGHTRED_EX + "INVALID INPUT. Please enter a valid numeric ID." + Fore.RESET)

#--------Status Divisor--------

        elif status == "CREATE_USER":

            while len(input_user) < 1 or len(input_user) > 15:
                input_user = input(Fore.LIGHTRED_EX + "Invalid username. The username must be between 1 and 15 characters.\n"+Fore.RESET+"Try again:")
                print()

            if self.client.menu_manager.check_username(input_user):

                self.client.username=input_user
                self.status_update = {"status": "CHECK_PASS_USER", "text": "\nEnter the password:"}

            else:

                self.status_update = {"status": "CREATE_USER", "text": "Try again with a different username. Enter the "+Fore.LIGHTGREEN_EX+"NEW USERNAME"+Fore.RESET+":"}

#--------Status Divisor--------
            
        elif status == "CHECK_PASS_USER":

            if not input_user:
                self.status_update = {"status": "CHECK_PASS_USER", "text": Fore.LIGHTRED_EX + "ERROR: Password cannot be empty. Please try again:" + Fore.RESET}
            elif input_user == "0":
                self.status_update = {"status": "CHECK_PASS_USER", "text": Fore.LIGHTRED_EX + "ERROR: Password cannot be 0. Please try again:" + Fore.RESET}
            elif len(input_user) > 15:
                self.status_update = {"status": "CHECK_PASS_USER", "text": Fore.LIGHTRED_EX + "ERROR: Password is too long. Maximum length is 15 characters. Please try again:" + Fore.RESET}
            else:
                self.client.password = input_user
                self.status_update = {"status": "SAVE_USER", "text": Fore.LIGHTGREEN_EX + "(OK)Valid password.\n"+Fore.RESET+"Do you want to save it?. Press ("+Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET+") to confirm  or "+Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET+" to cancel:"}
 
#--------Status Divisor--------
               
        elif status == "SAVE_USER":

            if input_user=="y" or input_user == "Y":

                self.client.user_data = {
                    "username": self.client.username,
                    "password": self.client.password
                }

                print("Sending the following data to create user:", json.dumps(self.client.user_data, indent=4).replace(
                    "username", f"{Fore.CYAN + 'username' + Fore.RESET}").replace(
                    "user_id", f"{Fore.CYAN + 'user_id' + Fore.RESET}").replace(
                    "password", f"{Fore.CYAN + 'password' + Fore.RESET}")
                )
                response = requests.post(url + "users/", json=self.client.user_data)   
                           
                if response.status_code == 200: 

                    print(f"Response Status: {Fore.LIGHTGREEN_EX }{response.status_code} OK!\n {Fore.RESET}")
                    response_data = response.json()  
                    self.client.user_id = response_data["user"].get("ID")  
                    self.client.username = response_data["user"].get("username")  
                    self.client.password = response_data["user"].get("password")  
                    self.status_update = {
                        "status": "MAIN", 
                        "text": f"{Fore.LIGHTGREEN_EX}User created successfully!\n{Fore.RESET}" + 
                                f"{Fore.CYAN}ID: {Fore.RESET} {self.client.user_id}.\n" + 
                                f"{Fore.CYAN}Username: {Fore.RESET} {self.client.username}.\n" + 
                                "\nEnter any key to continue:"
                    }

                else:

                    print(f"{Fore.LIGHTRED_EX }ERROR SAVING.{Fore.RESET}")
                    self.status_update = {"status": "EXIT", "text": f"Exiting"}

            else:
                    self.status_update = {"status": "NOT-LOGIN-MENU", "text": f"{Fore.LIGHTRED_EX + 'Operation cancelled.' + Fore.RESET}\nEnter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the login menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"}

#--------Status Divisor--------

        elif status == "MAIN":

            self.client.menu_manager.show_main_menu()
            self.status_update = {"status": "SELECT_OPC-MAIN_MENU", "text": f"Select an {Fore.LIGHTGREEN_EX}option{Fore.RESET}:"}
        
#--------Status Divisor--------

        elif status == "SELECT_OPC-MAIN_MENU":

            if input_user == "1":

                self.client.menu_manager.show_start_chat()
                self.status_update = {"status": "START_CHAT", "text": "Enter any char to init conversation:"}

            elif input_user == "2":

                print("Showing users...")
                print()
                response = requests.get(f"{url}users/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()
                self.status_update = {"status": "MAIN", "text": f"{Fore.LIGHTGREEN_EX}Enter any char to continue:{Fore.RESET}"}

            elif input_user == "3":

                print("Showing messages...")
                print()
                response = requests.get(f"{url}messages/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()
                self.status_update = {"status": "MAIN", "text": f"{Fore.LIGHTGREEN_EX}Enter any char to continue:{Fore.RESET}"}

            elif input_user == "0":
                
                self.status_update = {"status": "EXIT", "text": "saliendo."}
                
            else:
                print (f"{Fore.LIGHTRED_EX + 'INVALID OPTION' + Fore.RESET}. Try again.\n")

#--------Status Divisor--------
     
        elif status=="START_CHAT":    

            self.client.start_chat()
            self.status_update = {"status": "MAIN", "text": f"{Fore.LIGHTGREEN_EX}Enter any char to continue:{Fore.RESET}"}