import json
import websocket
import threading
from datetime import datetime
import time

message_received_event = threading.Event()

class ChatClient:
    def __init__(self):
        self.user_id = input("\nWelcome to chat-server!\n\nIngresa tu ID de usuario: ")
        
    def on_message(self, ws, message):
        try:
            msg_data = json.loads(message)
            content = msg_data['content']
            user_id_received = msg_data['user_id']  # Recibimos el ID de usuario
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"({current_time}) User {user_id_received}: {content}")
        except json.JSONDecodeError:
            print(f"Error al parsear el mensaje: {message}")

        message_received_event.set()

    def on_open(self, ws):
        print(f"\nHi, {self.user_id}!")
        message_received_event.set()
        # Iniciar la función de enviar mensajes una vez que la conexión esté abierta
        threading.Thread(target=self.send_message, args=(ws,), daemon=True).start()

    def on_close(self, ws, close_status_code, close_msg):
        print("Conexión cerrada\n")

    def on_error(self, ws, error):
        print(f"Error: {error}\n")

    def send_message(self, ws):
        while True:
            message_received_event.wait()  # Esperar a que el servidor envíe un mensaje primero
            message_received_event.clear()  # Resetear el evento
            time.sleep(0.2)
            msg = input(f"{self.user_id}: ")

            # Asegurarse de que `user_id` sea un entero
            message = {
                "user_id": int(self.user_id),  # Convertimos a entero
                "content": msg
            }
            ws.send(json.dumps(message))
            print(f"{self.user_id}: {msg}\n")

    def start_chat(self):
        ws = websocket.WebSocketApp("ws://localhost:8081/chat",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open

        # Ejecutar `run_forever` en un hilo separado
        wst = threading.Thread(target=ws.run_forever, daemon=True)
        wst.start()
        wst.join() 
        # Aquí podemos poner un ciclo para mantener el hilo principal activo
        

if __name__ == "__main__":
    client = ChatClient()
    client.start_chat()