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
#------------------------------------------------- Instance methods -----------------------------------------------------
    def __init__(self):
        print()
        print("----------------------------------")
        print("---- ¡Welcome to chat-server! ----")
        print("----------------------------------")
    
        self.register_ok = 0
        self.user_id = 0 
        self.username = MenuManager.request_username(self)
        
        while True:
            response = requests.get(f"{url}users/username/{self.username}")
            if response.status_code == 200:
                user_data = response.json() 
                self.user_id = user_data.get("user", {}).get("ID")
                self.username = user_data.get("user", {}).get("username") 
                self.password = user_data.get("user", {}).get("password") 
                in_password = MenuManager.request_pass(self)
                if (in_password=="0"):
                    break
                if MenuManager.check_password_hash(in_password, self.password):
                    print()
                    print("¡Successful registration!")
                    self.register_ok = 1
                    print("----------------------------------")
                    print(f"Hi, {self.username}!")
                    break
                else:
                    print("Incorrect password, please, try again!.")
            else:
                MenuManager.user_notfound_menu(self)
                break
                

        

    def on_message(self, ws, message):
        try:
            msg_data = json.loads(message)
            content = msg_data['content']
            user_id_received = msg_data['user_id']  
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"({current_time}){self.username}: {content}")
        except json.JSONDecodeError:
            print(f"Error parsing the message: {message}")

        message_received_event.set()

    def on_open(self, ws):
        message_received_event.set()
        #If the connection is open, this init send message function
        threading.Thread(target=self.send_message, args=(ws,), daemon=True).start()
        
    def on_close(self, ws, close_status_code, close_msg):
        print("Connection has been closed.\n")

    def on_error(self, ws, error):
        print(f"Error: {error}\n")

    def send_message(self, ws):
        while True:
            # Waiting for server msg
            message_received_event.clear()  
            time.sleep(0.2)

            #This is for delete the user line in console when the msg was sent
            sys.stdout.write(f"{self.username}: ")
            sys.stdout.flush()
            msg = input("")  
            sys.stdout.write("\033[F\033[K")  #Move the cursor up and delete the line.
            sys.stdout.flush()

            message = {
                "user_id": int(self.user_id),  
                "content": msg
            }
            selected_option =1 

            if msg.lower() == "./menu":
                while True:
                    selected_option = menu_manager_instance.show_app_menu_and_choose()
                    print(f"You selected option {selected_option}.")
                    if selected_option == 1:
                        print("Starting chat...")
                        print()
                        print("*********************************")
                        print("Use ./menu to return to the menu.")
                        print("*********************************")
                        print()
                        break
                    elif selected_option == 2:
                        print("Showing users...")
                        print()
                        response = requests.get(f"{url}users/") 
                        formatted_response = json.dumps(response.json(), indent=4)
                        print(formatted_response)
                    elif selected_option == 3:
                        print("Showing messages...")
                        print()
                        response = requests.get(f"{url}messages/") 
                        formatted_response = json.dumps(response.json(), indent=4)
                        print(formatted_response)
                    elif selected_option == 0:
                        print("Exiting...")
                        ws.close() 
                        return             
            else:
                ws.send(json.dumps(message)) #Send msg to WebSocketApp

            if selected_option==0:
                sys.exit() 
                      
    def start_chat(self):
        ws = websocket.WebSocketApp("ws://localhost:8081/chat", 
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open

        #Creating a new thread for run `run_forever` 
        wst = threading.Thread(target=ws.run_forever, daemon=True)
        wst.start()
        wst.join() 
    
#------------------------------------- CLIENT MAIN -----------------------------------------

if __name__ == "__main__":
    client = ChatClient() 
    menu_manager_instance = MenuManager(client)
    #client.menu_manager_instance = menu_manager_instance
    if client.register_ok==1:
        while True:
            selected_option = menu_manager_instance.show_app_menu_and_choose()
            menu_manager_instance.choice_function(selected_option, client)
        
    