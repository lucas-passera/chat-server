import json
import os
import sys
import requests
import websocket
import threading
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from client.menu_manager import MenuManager
import time
import colorama
from colorama import Back, Fore, Style

colorama.init(autoreset=True)
message_received_event = threading.Event()
url = "http://localhost:8081/"

class ChatClient:

#--------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        
        self.menu_manager = MenuManager(self)
        self.menu_manager.welcome()

        self.register_ok = 0  #This is to enter the main menu, if you logged in correctly.
        self.user_id = 0 
        self.username = MenuManager.request_username(self)
        
        while True:
            response = requests.get(f"{url}users/username/{self.username}") #get by username

            if response.status_code == 200:
                user_data = response.json() 

                self.user_id = user_data.get("user", {}).get("ID")
                self.username = user_data.get("user", {}).get("username") 
                self.password = user_data.get("user", {}).get("password")

                in_password = MenuManager.request_pass(self)    #This method returns the password entered by the user
                
                if (in_password=="0"):                           #exit opc
                    break

                if MenuManager.check_password_hash(in_password, self.password):    #Compare entered password with saved password (db)

                    print()
                    print("¡SUCCESSFUL REGISTRATION!")
                    print()
                    self.register_ok = 1     
                    print("----------------------------------")
                    print(f"Hi, {self.username}!")
                    break

                else:
                    print("Incorrect password, please, try again!.")

            else:  #USER NOT FOUND
                self.menu_manager.user_notfound_menu()
                
                break

#-------------------------------------------------------------------------------------------------------------------- 
               
    def on_message(self, ws, message):

        try:
            msg_data = json.loads(message)
            content = msg_data['content']  #extract message
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"({current_time}){self.username}: {content}")
            
        except json.JSONDecodeError:
            print(f"Error parsing the message: {message}")

        message_received_event.set()

#-------------------------------------------------------------------------------------------------------------------- 
      
    def on_open(self, ws):

        message_received_event.set()
        #If the connection is open, this init send message function
        threading.Thread(target=self.send_message, args=(ws,), daemon=True).start()

#--------------------------------------------------------------------------------------------------------------------  
             
    def on_close(self, ws, close_status_code, close_msg):
        print("Connection has been closed.\n")

#--------------------------------------------------------------------------------------------------------------------   
    
    def on_error(self, ws, error):
        print(f"Error: {error}\n")

#--------------------------------------------------------------------------------------------------------------------  
  
    def send_message(self, ws):

        while True:

            # Waiting for server msg
            message_received_event.clear()  
            time.sleep(0.2)

            #This is to delete the user's line in the console when the message is sent.
            sys.stdout.write(f"{self.username}: ")
            sys.stdout.flush()
            msg = input("")  
            sys.stdout.write("\033[F\033[K")  #Move the cursor up and delete the line.
            sys.stdout.flush()

            message = {
                "user_id": int(self.user_id),  
                "content": msg
            }

            if msg.lower() == "./menu":
                self.menu_manager.handle_chat_menu(url, ws)        
            else:
                ws.send(json.dumps(message)) #Send msg to WebSocketApp

#--------------------------------------------------------------------------------------------------------------------  
                           
    def start_chat(self):
        ws = websocket.WebSocketApp("ws://localhost:8081/chat", 
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open

        #Creating a new thread for run `run_forever`, open connection. 
        wst = threading.Thread(target=ws.run_forever, daemon=True)
        wst.start()
        wst.join() 

#--------------------------------------------------------------------------------------------------------------------      
#MAIN   
if __name__ == "__main__":

    client = ChatClient()  # Se crea la instancia de ChatClient

    if client.register_ok != 0:  # Verifica si el usuario se registró correctamente
        while True:
            selected_option = client.menu_manager.show_app_menu_and_choose()  # Accede al método desde client.menu_manager
            client.menu_manager.choice_function(selected_option, client)

#--------------------------------------------------------------------------------------------------------------------             
    