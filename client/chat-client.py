import json
import sys
import websocket
import threading
import time
import colorama
from datetime import datetime
from client.state_machine import StateMachine
from client.menu_manager import MenuManager
from colorama import Back, Fore, Style

colorama.init(autoreset=True)
message_received_event = threading.Event()
url = "http://localhost:8081/"

class ChatClient:

#--------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.ws = None 
        self.user_id = None  # o un valor por defecto
        self.username = None
        self.password = None
        self.user_data = {"user_id": self.user_id, "username": self.username, "password": self.password}
        self.menu_manager = MenuManager(self)
        self.menu_manager.welcome()

#-------------------------------------------------------------------------------------------------------------------- 

    def close_connection(self):
        if self.ws:
            self.ws.close()  # Cierra la conexión WebSocket si está abierta
            self.ws = None #reinicia para que no busque en la que estaba, la cual cerro 

#-------------------------------------------------------------------------------------------------------------------- 
               
    def on_message(self, ws, message):   #client receives msg

        try:
            msg_data = json.loads(message)
            content = msg_data['content']  #extract message
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"({current_time}) {Fore.LIGHTGREEN_EX}{self.username}{Fore.RESET}: {content}")
            
        except json.JSONDecodeError:
            print(Fore.RED + f"Error parsing the message: {message}")

        message_received_event.set()

#-------------------------------------------------------------------------------------------------------------------- 
      
    def on_open(self, ws):

        message_received_event.set()
        threading.Thread(target=self.send_message, args=(ws,), daemon=True).start()

#--------------------------------------------------------------------------------------------------------------------  
             
    def on_close(self, ws, close_status_code, close_msg):
        print()
        print(Fore.LIGHTRED_EX + "Connection has been closed.\n")

#--------------------------------------------------------------------------------------------------------------------   
    
    def on_error(self, ws, error):
        print(Fore.RED + f"Error: {error}\n")

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
                self.close_connection()
                break
            else:
                ws.send(json.dumps(message)) #Send msg to WebSocketApp

#--------------------------------------------------------------------------------------------------------------------   
                  
    def start_chat(self):

        if self.ws:  # Si ya hay una conexión abierta, la cerramos primero
            self.close_connection()

        self.ws = websocket.WebSocketApp("ws://localhost:8081/chat", 
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
        self.ws.on_open = self.on_open

        # Crear un nuevo hilo para ejecutar run_forever
        wst = threading.Thread(target=self.ws.run_forever, daemon=True)
        wst.start()
        wst.join()

#--------------------------------------------------------------------------------------------------------------------      
#MAIN   
if __name__ == "__main__":

    client = ChatClient()  
    state_machine = StateMachine(client)
    state_machine.run()
    
#--------------------------------------------------------------------------------------------------------------------             
    