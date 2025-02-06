package handlers

import (
	"log"
	"net/http"
	"sync"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
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
		// Esperamos que el cliente envíe un mensaje
		_, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("Error leyendo mensaje:", err)
			mu.Lock()
			delete(connections, conn)
			mu.Unlock()
			break
		}

		// Enviar el mensaje a todos los clientes conectados
		mu.Lock()
		for c := range connections {
			if err := c.WriteMessage(websocket.TextMessage, msg); err != nil {
				log.Println("Error enviando mensaje:", err)
			}
		}
		mu.Unlock()
	}
}
