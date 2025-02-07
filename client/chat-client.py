import json
import websocket
import threading
from datetime import datetime

message_received_event = threading.Event()
username = ""

# Función para manejar los eventos de mensaje
def on_message(ws, message):

    try:
        msg_data = json.loads(message)
        content = msg_data['content']
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"({current_time}){username}:",content)
    except json.JSONDecodeError:
        print(f"Error al parsear el mensaje: {message}")
    
    message_received_event.set()

def on_open(ws):
    global username
    print(f"\nHi, {username}!")

    message_received_event.set()
# Función para manejar los eventos de cierre
def on_close(ws, close_status_code, close_msg):
    print("Conexión cerrada\n")

# Función para manejar los eventos de error
def on_error(ws, error):
    print(f"Error: {error}\n")

# Función para enviar mensajes en un hilo separado
def send_message(ws, username):
    while True:
        message_received_event.wait()  # Esperar antes de pedir otro mensaje
        message_received_event.clear()  # Resetear el evento

        msg = input(f"{username}: ") 
        
        message = {
            "user_id": 1,
            "content": msg
        }
        ws.send(json.dumps(message))
        
        # Resetear el evento para esperar la próxima recepción de mensaje
        message_received_event.clear()

# Iniciar la conexión WebSocket y ejecutar en segundo plano
def start_chat():
    global username
    username = input("\nWelcome to chat-server!\n\nIngresa tu nombre de usuario: ")

    ws = websocket.WebSocketApp("ws://localhost:8081/chat",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Ejecutar `run_forever` en un hilo separado
    wst = threading.Thread(target=ws.run_forever, daemon=True)
    wst.start()

    # Iniciar la función de enviar mensajes en el hilo principal
    send_message(ws, username)

if __name__ == "__main__":
    start_chat()