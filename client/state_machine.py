import json
import requests

url = "http://localhost:8081/"

class StateMachine:
    
    def __init__(self, client):
        self.client = client
        self.menu_manager = client.menu_manager
        self.status_update = {"status": "INIT", "text": "Ingrese un usuario:"}
        print("Welcome to chat server!")

    def run(self):
        while self.status_update["status"] != "EXIT":
            print(self.status_update["text"])  
            input_user = input("> ").strip()
            self.processInput(input_user)

    def processInput(self, input_user):
        status = self.status_update["status"]

        if status == "INIT":
            response = requests.get(f"{url}users/username/{input_user}")
            if response.status_code == 200:
                self.client.user_data = response.json()
                self.status_update = {"status": "LOGIN_REQUEST_PASS", "text": "Ingrese su contraseña:"}
            else:
                self.status_update = {"status": "NOT-LOGIN-MENU", "text": "Usuario no encontrado. Seguir intentando? (Y/N)"}

        elif status == "LOGIN_REQUEST_PASS":
            if input_user == "0":
                self.status_update = {"status": "EXIT", "text": "Saliendo..."}
            elif self.menu_manager.check_password_hash(input_user, self.client.user_data["password"]):
                print("")
                self.status_update = {"status": "MAIN", "text": "¡Inicio de sesión exitoso!"}
            else:
                print("Contraseña incorrecta. Inténtelo de nuevo.")
        
        elif status == "NOT-LOGIN-MENU":
            if input_user=="y":
                print("1-Try again.")
                print("2-Enter with ID.")
                print("3-Create a new user.")
                print("0-Exit.\n")
                self.status_update = {"status": "SELECT_OPC-NOT_FOUND_MENU", "text": "Select an option: "}
            else:
                self.status_update = {"status": "EXIT", "text": "Exiting..."}

        elif status == "SELECT_OPC-NOT_FOUND_MENU":
            if input_user == "1":
                self.status_update = {"status": "INIT", "text": "Ingrese un usuario:"}
            elif input_user == "2":
                self.status_update = {"status": "ENTER_WITH_ID", "text": "Ingrese ID:"}
            elif input_user == "3":
                self.status_update = {"status": "CREATE_USER", "text": "Ingrese nuevo usuario:"}
            elif input_user == "0":
                self.status_update = {"status": "EXIT", "text": "Saliendo del sistema..."}
            else:
                self.status_update = {"status": "NOT-LOGIN-MENU", "text": "Opción no válida. Intente de nuevo."}

        elif status == "CREATE_USER":
            if self.client.check_username(input_user):
                self.username=input_user
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
                self.password=input_user
                self.status_update = {"status": "SAVE_USER", "text": "Correct password, do you want to save it ?(y/n)"}
                

        elif status == "SAVE_USER":
            if input_user=="y":
                data = {"username": self.username, "password": self.password}
                response = requests.post(url + "users/", json=data)                
                if response.status_code == 200: 
                    response_data = response.json()  
                    user_id = response_data["user"].get("ID")  
                    self.status_update = {"status": "MAIN", "text": f"User created successfully with ID: {user_id}, Continue? (Y/N)"}

                else:
                    self.status_update = {"status": "EXIT", "text": f"ERROR GUARDANDO, SALIENDO POR SEGURIDAD.."}

        elif status == "MAIN":
            print("----------------------------------\n")
            print()
            print("1-Chat.")
            print("2-Users.")
            print("3-Messages.")
            print("0-Exit.")
            print("\n----------------------------------\n")
            print("")
            self.status_update = {"status": "SELECT_OPC-MAIN_MENU", "text": "Seleccione una opción:"} 

        elif status == "SELECT_OPC-MAIN_MENU":
            if input_user == 1:
                print("Starting chat...")
                print()
                print("**********************************")
                print("Use ./menu to return to the menu.")
                print("**********************************")
                print()
                self.client.start_chat()
                self.status_update = {"status": "MAIN", "text": "Finalizando el chat..."}

            elif input_user == 2:

                print("Showing users...")
                print()
                response = requests.get(f"{url}users/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()

            elif input_user == 3:

                print("Showing messages...")
                print()
                response = requests.get(f"{url}messages/") 
                formatted_response = json.dumps(response.json(), indent=4)
                print(formatted_response)
                print()

            elif input_user == 0:
                print("Exiting...")
                print()
                self.status_update = {"status": "EXIT", "text": "Seleccione una opción:"} 

        #elif status == "ENTER_WITH_ID":
        #    user_id = self.menu_manager.request_id()
        #    response = requests.get(f"{url}users/{self.user_id}")
        #    if response.status_code == 200:
        #        user_data = response.json() 
        #        self.user_id = user_data.get("user", {}).get("ID")
        #        self.username = user_data.get("user", {}).get("username") 
        #        self.password = user_data.get("user", {}).get("password") 
        #        self.status_update = {"status": "USER_FOUND_WITH_ID", "text": "Usuario encontrado, ingrese su contraseña:"}
#
        #        
        #    
#
        #            
        #     
#
        #    else:
        #        self.status_update = {"status": "ENTER_WITH_ID", "text": "Eligio ingresar con ID."}
        #        
        #elif status == "USER_FOUND_WITH_ID":  
        #    in_password = MenuManager.request_pass(self)
#
        #    if (in_password=="0"):
        #        self.register_ok=0
        #        return self.register_ok
        #            
#
        #    if MenuManager.check_password_hash(in_password, self.password):
        #        print("¡SUCCESSFUL REGISTRATION!")
        #        self.register_ok = 1
        #        print("----------------------------------")
        #        print(f"¡Hi, {self.username}!")
        #        option=1
        #        return self.register_ok
        #    else:
        #        print("Incorrect password, please, try again.")
