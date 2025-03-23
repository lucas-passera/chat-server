import json
import sys
from colorama import Fore
from DisplayManager import DisplayManager
import requests

#url="http://184.72.171.214:8081/"
url="http://localhost:8081/"
class StateMachine:

    LOGIN_MENU = "LOGIN_MENU"
    SELECT_OPC_LOGIN_MENU = "SELECT_OPC_LOGIN_MENU"
    LOGIN_REQUEST_PASS = "LOGIN_REQUEST_PASS"
    MAIN = "MAIN"
    EXIT = "EXIT"
    ENTER_WITH_USERNAME = "ENTER_WITH_USERNAME"
    ENTER_WITH_ID = "ENTER_WITH_ID"
    CREATE_USER = "CREATE_USER"
    START_CHAT = "START_CHAT"
    SELECT_OPC_MAIN_MENU = "SELECT_OPC_MAIN_MENU"
    SAVE_USER = "SAVE_USER"
    CHECK_PASS_USER = "CHECK_PASS_USER"
    USERNAME_LEN_VALIDATOR = "USERNAME_LEN_VALIDATOR"

#--------------------------------------------------------------------------------------------------------------------    

    def __init__(self, client):
        self.displayManager = DisplayManager()
        self.current_status = {
            "code": "", # if a state doesn't need this, only send empty string.
            "status": self.LOGIN_MENU,
            "text": f"Enter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the login menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"
        }
        self.client=client

#--------------------------------------------------------------------------------------------------------------------
  
    def update_status(self, code, status, text):
        self.current_status = {"code": code, "status": status, "text": text}
        return self.current_status

#--------------------------------------------------------------------------------------------------------------------
                
    def run(self):
        while self.current_status["status"] != self.EXIT:
            print(self.current_status["text"])  
            input_user = input("> ").strip()
            print()
            new_state = self.processInput(input_user)
        print(Fore.LIGHTGREEN_EX+"Exiting..."+Fore.RESET)
        sys.exit()

#-------------------------------------------------------------------------------------------------------------------- 
       
    def processInput(self, input_user):

        current_status = self.current_status["status"]

#--------Status Divisor--------

        if current_status == self.LOGIN_MENU:

            if input_user=="y" or input_user == "Y":
                self.displayManager.show_login_menu()
                self.current_status = self.update_status("", self.SELECT_OPC_LOGIN_MENU, f"Select an {Fore.LIGHTGREEN_EX}OPTION{Fore.RESET}:")
                return self.current_status

            else:
                self.current_status = self.update_status("", self.EXIT, "Exiting...")
                return self.current_status

#--------Status Divisor--------

        elif current_status == self.SELECT_OPC_LOGIN_MENU:

            if input_user == "1":
                self.current_status = self.update_status("", self.ENTER_WITH_USERNAME, "Enter your " + Fore.LIGHTGREEN_EX + "USERNAME" + Fore.RESET + " or " +
                        Fore.LIGHTGREEN_EX + "0" + Fore.RESET + " to exit:")                
                return self.current_status
            elif input_user == "2":
                self.current_status = self.update_status("", self.ENTER_WITH_ID, "\nEnter your " + Fore.LIGHTGREEN_EX + "USER ID" + Fore.RESET + " or " +
                        Fore.LIGHTGREEN_EX + "0" + Fore.RESET + " to cancel:")                                
                return self.current_status
            elif input_user == "3":
                self.current_status = self.update_status("", self.CREATE_USER, "Enter a "+Fore.LIGHTGREEN_EX+"NEW USERNAME"+Fore.RESET+":")   
                return self.current_status
            elif input_user == "0":
                self.current_status = self.update_status("", self.EXIT, "Exiting...") 
                return self.current_status
            else:
                self.current_status = self.update_status("INVALID OPTION", self.SELECT_OPC_LOGIN_MENU, Fore.LIGHTRED_EX + 'INVALID OPTION' + Fore.RESET + "\nEnter 'Y' to try again o 'ANY KEY' to exit.")
                return self.current_status
                
#--------Status Divisor--------

        elif current_status == self.ENTER_WITH_USERNAME:

            username = self.username_length_validator(input_user)

            if username == "0":
                self.current_status = self.update_status(
                    "EXIT",
                    self.EXIT,
                    "exiting"
                )
                return self.current_status
            else:
                response = requests.get(f"{url}users/username/{username}")

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

                    self.current_status = self.update_status(
                        response.status_code,
                        self.LOGIN_REQUEST_PASS,
                        "Enter your password:"
                    )

                    print("User found:\n" + Fore.CYAN + f"ID: {self.client.user_data.get('user_id')}, Username: {self.client.user_data.get('username')}\n")
                    return self.current_status
                else:

                    if response.status_code == 404:
                        print("Response Status:", Fore.LIGHTRED_EX + str(response.status_code) + Fore.RESET)

                        self.current_status = self.update_status(
                            response.status_code,
                            self.LOGIN_MENU,
                            f"{Fore.LIGHTRED_EX + 'USER NOT FOUND.' + Fore.RESET} \n\nEnter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the program menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"
                        )

                        return self.current_status

                    elif response.status_code == 400: 

                        print("Response Status:", Fore.LIGHTRED_EX + str(response.status_code) +" BAD REQUEST "+ Fore.RESET)

                        self.current_status = self.update_status(
                            response.status_code,
                            self.LOGIN_MENU,
                            f"\nEnter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the login menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"
                        )

                        return self.current_status

                    else:

                        print("Response Status:", Fore.LIGHTRED_EX + str(response.status_code) + Fore.RESET)
                        self.current_status = self.update_status(
                            response.status_code,
                            self.EXIT,
                            "Exiting..."
                        )

                        self.current_status = self.update_status(
                            response.status_code,
                            self.LOGIN_MENU,
                            f"\nEnter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the login menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"
                        )
                        return self.current_status

#--------Status Divisor--------

        elif current_status == self.LOGIN_REQUEST_PASS:
            username = self.client.user_data.get("username")
            password = input_user

            if password == "0":
                self.current_status = self.update_status(
                    "EXIT",
                    self.EXIT,
                    "Exiting..."
                )
                return self.current_status
            
            else:
                url_aux = "http://localhost:8081/users/check-password"
                data = {
                "username": username,
                "password": password
                }   
                response = requests.post(url_aux, json=data)            
                if response.status_code == 200:
                        self.current_status = self.update_status (
                        response.status_code,
                        self.MAIN,
                        f"{Fore.LIGHTGREEN_EX + '¡Registration completed successfully!' + Fore.RESET}. \n\nEnter any char to continue:"
                             )
                        return self.current_status
            
                elif response.status_code == 400:
                    self.current_status = self.update_status(
                        response.status_code,
                        self.LOGIN_REQUEST_PASS,
                        Fore.LIGHTRED_EX + "Bad request, invalid data." + Fore.RESET + "\nPlease try again or enter ("+Fore.LIGHTGREEN_EX+ "0" +Fore.RESET+") to exit."

                    )
                    return self.current_status
                
                else: 
                    self.current_status = self.update_status(
                        response.status_code,
                        self.LOGIN_REQUEST_PASS,
                        Fore.LIGHTRED_EX + "Incorrect password." + Fore.RESET + "\nPlease try again or enter ("+Fore.LIGHTGREEN_EX+ "0" +Fore.RESET+") to exit."

                    )
                    return self.current_status

#--------Status Divisor--------

        elif current_status == self.ENTER_WITH_ID:

            try:

                input_user = int(input_user)  

                if input_user == 0:

                    self.current_status = self.update_status (
                        "CANCEL ENTER WITH ID",
                        self.LOGIN_MENU,
                        f"Canceling... press ({Fore.LIGHTGREEN_EX}Y{Fore.RESET}) to return to the registration menu or ({Fore.LIGHTGREEN_EX}ANY KEY{Fore.RESET}) to exit."
                    )
                    return self.current_status
                    
                elif 0 < input_user < 10000:  # [0 < ID USER < 9999]

                    response = requests.get(f"{url}users/{input_user}")

                    if response.status_code == 200:

                        print("Response Status:", Fore.LIGHTGREEN_EX + str(response.status_code) + " OK" + Fore.RESET)

                        user_data = response.json()["user"]    # json's server

                        self.client.user_data = {  #guardo solo lo que me interesa aca
                            "user_id": user_data.get("ID"),
                            "username": user_data.get("username"),
                            "password": user_data.get("password")
                        }

                        self.client.user_id = user_data.get("ID")  # Sincronizamos
                        self.client.username = user_data.get("username")

                        self.current_status = self.update_status (
                            response.status_code,
                            self.LOGIN_REQUEST_PASS,
                            "User found:\n" + Fore.CYAN + f"ID: {self.client.user_data.get('user_id')}, Username: {self.client.user_data.get('username')}.\nEnter your password:"
                        )

                        return self.current_status
                    
                    else:
                        self.current_status = self.update_status(
                            response.status_code,
                            self.LOGIN_MENU,
                            f"User not found, press ({Fore.LIGHTGREEN_EX}Y{Fore.RESET}) to return to the registration menu or ({Fore.LIGHTGREEN_EX}ANY KEY{Fore.RESET}) to exit."
                        )
                        return self.current_status
                    
                else:
                    self.current_status = self.update_status(
                        "INVALID RANGE ID",
                        self.ENTER_WITH_ID,
                        Fore.LIGHTRED_EX + "INVALID ID." + Fore.RESET + " (ID MUST BE IN THIS RANGE: 0<ID<10000).\nTry again. "
                    )
                    return self.current_status

            except ValueError:  #if input user is not a number
                self.current_status = self.update_status(
                        "INVALID INPUT",
                        self.ENTER_WITH_ID,
                        Fore.LIGHTRED_EX + "INVALID INPUT. Please enter a valid NUMERIC ID." + Fore.RESET
                )                 
                return self.current_status

#--------Status Divisor--------

        elif current_status == self.CREATE_USER:
            username = self.username_length_validator(input_user)
            urlAux = f"http://localhost:8081/users/check-username/{username}"  #LOCAL
            #url = f"http://184.72.171.214:8081/users/check-username/{username}"
            
            try:
                response = requests.get(urlAux)
                if response.status_code == 200:
                    print("Username is "+Fore.LIGHTGREEN_EX+"available"+Fore.RESET)
                    self.client.username=username
                    self.current_status = self.update_status(
                        response.status_code,
                        self.CHECK_PASS_USER,
                        "Enter a password or 0 to exit:"
                        )
                    return self.current_status
                elif response.status_code == 409:

                    print(Fore.LIGHTRED_EX+"Username already exists. "+Fore.RESET+"\n")

                    self.current_status = self.update_status(
                        response.status_code,
                        self.CREATE_USER,
                        "Try again with a different username. Enter the "+Fore.LIGHTGREEN_EX+"NEW USERNAME"+Fore.RESET+":"
                        )
                    
                    return self.current_status
                
                else:
                    self.current_status = self.update_status(
                        response.status_code,
                        self.CREATE_USER,
                        "Try again with a different username. Enter the "+Fore.LIGHTGREEN_EX+"NEW USERNAME"+Fore.RESET+":"
                        )
                    print(f"{Fore.LIGHTRED_EX}Error:{Fore.RESET} {response.status_code}, Could not check username")
                    return self.current_status
                
            except requests.exceptions.RequestException as e:
                print(f"{Fore.LIGHTRED_EX}Error connecting to server:{Fore.RESET} {e}")
                self.current_status = self.update_status(
                        requests.exceptions.RequestException,
                        self.EXIT,
                        "Exiting..."
                        )
                return self.current_status

                
            
#--------Status Divisor--------
            
        elif current_status == self.CHECK_PASS_USER:
            self.client.password = input_user
            if not self.client.password:
                self.current_status = self.update_status(
                    "EMPTY PASSWORD",
                    self.CHECK_PASS_USER,
                    Fore.LIGHTRED_EX + "ERROR: Password cannot be empty. Please try again:" + Fore.RESET
                )
                return self.current_status
            
            elif self.client.password == "0":
                self.current_status = self.update_status(
                    "EXIT",
                    self.EXIT,
                    "Exiting..."
                )
                return self.current_status 
            
            elif len(self.client.password)>15:

                self.current_status = self.update_status(
                    "PASSWORD TOO LONG",
                    self.CHECK_PASS_USER,
                    Fore.LIGHTRED_EX + "ERROR: Password is too long. Maximum length is 15 characters. Please try again:" + Fore.RESET
                )
                return self.current_status 
            
            else:
                self.current_status = self.update_status(
                    "VALID PASSWORD",
                    self.SAVE_USER,
                    Fore.LIGHTGREEN_EX + "(OK)Valid password.\n"+Fore.RESET+"Do you want to save it?. Press ("+Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET+") to confirm  or "+Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET+" to cancel:"
                )
                return self.current_status 
            
#--------Status Divisor--------

        elif current_status == self.SAVE_USER:

            if input_user=="y" or input_user == "Y":

                self.client.user_data = {
                    "user_id": self.client.user_id,
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
                    self.current_status = self.update_status (
                        response.status_code,
                        self.MAIN, 
                        f"{Fore.LIGHTGREEN_EX}User created successfully!\n{Fore.RESET}" + 
                        f"{Fore.CYAN}ID: {Fore.RESET} {self.client.user_id}.\n" + 
                        f"{Fore.CYAN}Username: {Fore.RESET} {self.client.username}.\n" + 
                        "\nEnter any key to continue:"
                    )
                    return self.current_status

                else:

                    print(f"{Fore.LIGHTRED_EX }ERROR SAVING.{Fore.RESET}")
                    self.current_status = self.update_status(
                        response.status_code,
                        self.EXIT, 
                        "Exiting")
                    
                    return self.current_status
            else:
                self.current_status = self.update_status(
                    "CANCEL SAVE USER",
                    self.LOGIN_MENU,
                    f"{Fore.LIGHTRED_EX + 'Operation cancelled.' + Fore.RESET}\nEnter ({Fore.LIGHTGREEN_EX + 'Y' + Fore.RESET}) to access the login menu or {Fore.LIGHTGREEN_EX + 'ANY KEY' + Fore.RESET} to exit:"
                )
                return self.current_status
            
#--------Status Divisor--------

        elif current_status == self.MAIN:
            self.displayManager.show_main_menu()
            self.current_status = self.update_status (
                "",
                self.SELECT_OPC_MAIN_MENU, 
                f"Select an {Fore.LIGHTGREEN_EX}option{Fore.RESET}:"
            )
            return self.current_status
        
#--------Status Divisor--------

        elif current_status == self.SELECT_OPC_MAIN_MENU:

            if input_user == "1":

                self.displayManager.show_start_chat()
                self.current_status = self.update_status(
                    "START CHAT",
                    self.START_CHAT,
                    "Enter any char to init conversation:"
                    )
                return self.current_status
            
            elif input_user == "2":

                print("Showing users...")
                print()
                response = requests.get(f"{url}users/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()
                self.current_status = self.update_status(
                    response.status_code,
                    self.MAIN,
                    f"{Fore.LIGHTGREEN_EX}Enter any char to continue:{Fore.RESET}"
                ) 
                return self.current_status
            
            elif input_user == "3":

                print("Showing messages...\n")
                response = requests.get(f"{url}messages/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()
                self.current_status = self.update_status(
                    response.status_code,
                    self.MAIN,
                    f"{Fore.LIGHTGREEN_EX}Enter any char to continue:{Fore.RESET}"
                ) 
                return self.current_status
            
            elif input_user == "0": 
                self.current_status = self.update_status(
                    "EXIT",
                    self.EXIT,
                    "Exiting..."
                )
                return self.current_status
                
            else:
                self.current_status = self.update_status("INVALID OPTION", self.MAIN, Fore.LIGHTRED_EX + 'INVALID OPTION' + Fore.RESET + "\nEnter 'ANY KEY' to continue. ")           
                return self.current_status
            
#--------Status Divisor--------
     
        elif current_status==self.START_CHAT:    
            self.client.start_chat()
            self.current_status = self.update_status(
                "",
                self.MAIN,
                f"{Fore.LIGHTGREEN_EX}Enter any char to continue:{Fore.RESET}"
            )

#--------------------------------------------------------------------------------------------------------------------

    def username_length_validator(self, input_user):
        while input_user != "0" and len(input_user) < 1 or len(input_user) > 15:
            input_user = input(Fore.LIGHTRED_EX + "Invalid username. The username must be between 1 and 15 characters.\n" + Fore.RESET + "\nTry again with a different password or enter '0' to exit:\n")
            
            
        return input_user
    
#--------------------------------------------------------------------------------------------------------------------
    