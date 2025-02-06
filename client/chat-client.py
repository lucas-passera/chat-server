import json
import websocket
import threading

# Evento para sincronizar la conexión y los mensajes recibidos
message_received_event = threading.Event()

# Función para manejar los eventos de mensaje
def on_message(ws, message):
    # Parsear el mensaje recibido (asumiendo que es un JSON)
    try:
        msg_data = json.loads(message)
        # Mostrar solo el contenido del mensaje
        print(f"Mensaje en el servidor: {msg_data['content']}\n")
    except json.JSONDecodeError:
        print(f"Error al parsear el mensaje: {message}")
    
    message_received_event.set()  # Notificar que un mensaje ha sido recibido
# Función para manejar los eventos de conexión
def on_open(ws):
    print("Conectado al servidor de chat\n")
    message_received_event.set()  # Notificar que la conexión está abierta

# Función para manejar los eventos de cierre
def on_close(ws, close_status_code, close_msg):
    print("Conexión cerrada\n")

# Función para manejar los eventos de error
def on_error(ws, error):
    print(f"Error: {error}\n")

# Función para enviar mensajes en un hilo separado
def send_message(ws):
    while True:
        # Esperar a que un mensaje haya sido recibido antes de pedir otro
        message_received_event.wait()
        msg = input("You: ")
        
        message = {
            "user_id": 1,
            "content": msg
        }
        ws.send(json.dumps(message))
        print(f"Mensaje enviado!")
        
        # Resetear el evento para esperar la próxima recepción de mensaje
        message_received_event.clear()

# Iniciar la conexión WebSocket y ejecutar en segundo plano
def start_chat():
    ws = websocket.WebSocketApp("ws://localhost:8081/chat",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Ejecutar `run_forever` en un hilo separado
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    # Iniciar la función de enviar mensajes en el hilo principal
    send_message(ws)

if __name__ == "__main__":
    start_chat()