package handlers

import (
	"log"
	"net/http"
	"sync"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"github.com/lucas-passera/chat-server/entities"
	"github.com/lucas-passera/chat-server/repository"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

var connections = make(map[*websocket.Conn]bool) // Conexiones activas de WebSocket
var mu sync.Mutex

// ChatHandler maneja la conexión WebSocket
func ChatHandler(c *gin.Context) {
	conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		log.Println("Error upgrading connection:", err)
		return
	}
	defer conn.Close()

	mu.Lock()
	connections[conn] = true
	mu.Unlock()

	log.Println("Nuevo cliente conectado")

	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("Error leyendo mensaje:", err)
			mu.Lock()
			delete(connections, conn)
			mu.Unlock()
			break
		}

		// Crear el mensaje con el contenido recibido como texto
		message := entities.Message{
			UserID:  1,           // Supón que el UserID es 1 para este ejemplo, en producción tomarías este valor de alguna forma
			Content: string(msg), // El mensaje recibido como texto
		}

		// Guardar el mensaje en la base de datos
		if err := repository.CreateMessage(&message); err != nil {
			log.Println("Error guardando mensaje:", err)
		} else {
			log.Println("Mensaje guardado con éxito")
		}

		// Reenviar el mensaje a todos los clientes conectados
		mu.Lock()
		for c := range connections {
			if err := c.WriteMessage(websocket.TextMessage, msg); err != nil {
				log.Println("Error enviando mensaje:", err)
			}
		}
		mu.Unlock()
	}
}
