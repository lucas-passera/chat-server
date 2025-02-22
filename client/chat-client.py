import json
import os
import sys
import requests
import websocket
import threading
from datetime import datetime

from client.state_machine import StateMachine
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
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
        self.user_id = None  # o un valor por defecto
        self.username = None
        self.password = None
        self.user_data = {"user_id": self.user_id, "username": self.username, "password": self.password}
        self.menu_manager = MenuManager(self)
        self.menu_manager.welcome()
        
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
                "user_id": int(self.user_data["user_id"]),  
                "content": msg
            }

            if msg.lower() == "./menu":
                print("\nSaliendo del chat y volviendo al menú...\n")
                ws.close()
                break
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

    client = ChatClient()  
    state_machine = StateMachine(client)
    state_machine.run()
#--------------------------------------------------------------------------------------------------------------------             
    