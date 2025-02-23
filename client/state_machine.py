import json
import sys
import bcrypt
from colorama import Fore
import requests

url = "http://localhost:8081/"

class StateMachine:
    
    def __init__(self, client):
        self.client = client
        self.status_update = {
            "status": "NOT-LOGIN-MENU",
            "text": f"Presione {Fore.YELLOW + 'Y' + Fore.RESET} para acceder al menú del programa o {Fore.YELLOW + 'CUALQUIER TECLA' + Fore.RESET}  para salir:"
        }

    def run(self):
        while self.status_update["status"] != "EXIT":
            print(self.status_update["text"])  
            input_user = input("> ").strip()
            print()
            self.processInput(input_user)
        sys.exit()
        
    def processInput(self, input_user):
        status = self.status_update["status"]
        
        if status == "ENTER_WITH_USERNAME":
            response = requests.get(f"{url}users/username/{input_user}")
            if response.status_code == 200:
                print("Response Status:", Fore.GREEN + str(response.status_code) + Fore.RESET)
                self.client.user_data = response.json()["user"]
                self.client.user_data = {  # Modificamos directamente la propiedad de ChatClient
                    "user_id": self.client.user_data.get("ID"),
                    "username": self.client.user_data.get("username"),
                    "password": self.client.user_data.get("password")
                }
                self.client.user_id = self.client.user_data.get("ID")  # Sincronizamos
                self.client.username = self.client.user_data.get("username")
                
                self.status_update = {"status": "LOGIN_REQUEST_PASS", "text": "Ingrese su contraseña:"}
            else:
                print("Response Status:", Fore.LIGHTRED_EX + str(response.status_code) + Fore.RESET)
                self.status_update = {
                    "status": "NOT-LOGIN-MENU",
                    "text": f"{Fore.LIGHTRED_EX + 'USUARIO NO ENCONTRADO.' + Fore.RESET} \n\nPresione {Fore.YELLOW + 'Y' + Fore.RESET} para acceder al menú del programa o {Fore.YELLOW + 'CUALQUIER TECLA' + Fore.RESET}  para salir:"
                }
                

        elif status == "LOGIN_REQUEST_PASS":
            if input_user == "0":
                self.status_update = {"status": "EXIT", "text": "Saliendo..."}
            elif bcrypt.checkpw(input_user.encode(), self.client.user_data["password"].encode()):
                print("Inicio de sesión exitoso")
                self.status_update = {"status": "MAIN", "text": "¡Inicio de sesión exitoso! Presione alguna tecla para continuar. "}
            else:
                print("Contraseña incorrecta. Inténtelo de nuevo.")
        
        elif status == "NOT-LOGIN-MENU":
            if input_user=="y":
                print("1-Enter with Username.")
                print("2-Enter with ID.")
                print("3-Create a new user.")
                print("0-Exit.\n")
                self.status_update = {"status": "SELECT_OPC-NOT_FOUND_MENU", "text": "Select an option: "}
            else:
                self.status_update = {"status": "EXIT", "text": "Exiting..."}

        elif status == "SELECT_OPC-NOT_FOUND_MENU":
            if input_user == "1":
                self.status_update = {"status": "ENTER_WITH_USERNAME", "text": "Ingrese un usuario:"}
            elif input_user == "2":
                self.status_update = {"status": "ENTER_WITH_ID", "text": "Elegio ingresar con ID, desea continuar? (Y/N):"}
            elif input_user == "3":
                self.status_update = {"status": "CREATE_USER", "text": "Ingrese nuevo usuario:"}
            elif input_user == "0":
                self.status_update = {"status": "EXIT", "text": "Saliendo del sistema..."}
            else:
                self.status_update = {"status": "NOT-LOGIN-MENU", "text": "Opción no válida. Intente de nuevo."}

        elif status == "CREATE_USER":
            if self.client.menu_manager.check_username(input_user):
                self.client.username=input_user
                self.status_update = {"status": "CHECK_PASS_USER", "text": "Username available, enter the password:"}
            else:
                self.status_update = {"status": "CREATE_USER", "text": "Try again with a different username. Enter the username:"}
            
        elif status == "CHECK_PASS_USER":
            if not input_user:
                self.status_update = {"status": "CHECK_PASS_USER", "text": "Password cannot be empty. Please try again:"}
            elif input_user=="0":
                self.status_update = {"status": "CHECK_PASS_USER", "text": "Password cannot be 0. Please try again:"}
            elif len(input_user) > 15:
                self.status_update = {"status": "CHECK_PASS_USER", "text": "Password is too long. Maximum length is 15 characters. Please try again:"}
            else:
                self.client.password=input_user
                self.status_update = {"status": "SAVE_USER", "text": "Correct password, do you want to save it ?(y/n)"}
                

        elif status == "SAVE_USER":
            if input_user=="y":
                self.client.user_data = {
                    "username": self.client.username,
                    "password": self.client.password
                }

                print("Enviando los siguientes datos para crear usuario:", json.dumps(self.client.user_data, indent=4))
                response = requests.post(url + "users/", json=self.client.user_data)   
                print(f"Respuesta del servidor: {response.status_code} - {response.text}")  # Depuración             
                if response.status_code == 200: 
                    response_data = response.json()  
                    self.client.user_id = response_data["user"].get("ID")  
                    self.status_update = {"status": "MAIN", "text": f"User created successfully with ID: {self.client.user_id}, Continue? (Y/N)"}

                else:
                    print("error guardando")
                    self.status_update = {"status": "EXIT", "text": f"ERROR GUARDANDO, SALIENDO POR SEGURIDAD.."}

        elif status == "MAIN":
            print("----------------------------------\n")
            print("1-Chat.")
            print("2-Users.")
            print("3-Messages.")
            print("0-Exit.")
            print("\n----------------------------------\n")
            self.status_update = {"status": "SELECT_OPC-MAIN_MENU", "text": "Seleccione una opción:"} 

        elif status == "SELECT_OPC-MAIN_MENU":
            if input_user == "1":
                print("Starting chat...")
                print()
                print("**********************************")
                print("Use ./menu to return to the menu.")
                print("**********************************")
                print()
                self.status_update = {"status": "START_CHAT", "text": ""}

            elif input_user == "2":

                print("Showing users...")
                print()
                response = requests.get(f"{url}users/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()
                self.status_update = {"status": "MAIN", "text": "Volviendo al menu... presione alguna tecla para continuar"}

            elif input_user == "3":

                print("Showing messages...")
                print()
                response = requests.get(f"{url}messages/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()
                self.status_update = {"status": "MAIN", "text": "Volviendo al menu... presione alguna tecla para continuar"}

            elif input_user == "0":
                print("Exiting...")
                print()
                self.status_update = {"status": "EXIT", "text": "saliendo."}

        elif status == "ENTER_WITH_ID":
            if(input_user=="y"):
                self.client.user_id = self.client.menu_manager.request_id()
                response = requests.get(f"{url}users/{self.client.user_id}")
                if response.status_code == 200:
                    print("Response Status:", response.status_code)
                    print("Response JSON:", response.json())
                    self.client.user_data = response.json()["user"]
                    self.status_update = {"status": "LOGIN_REQUEST_PASS", "text": "Usuario encontrado, ingrese su contraseña:"}
                else:
                    self.status_update = {"status": "NOT-LOGIN-MENU", "text": "Usuario no encontrado, presione (Y) para volver al menu u otra tecla para salir."}
            else:
                self.status_update = {"status": "NOT-LOGIN-MENU", "text": "Cancelando... presione (Y) para volver al menu u otra tecla para salir."}
     
        elif status=="START_CHAT":      
            self.client.start_chat()
            self.status_update = {"status": "MAIN", "text": "Volviendo al menú. Presione alguna tecla para continuar."}