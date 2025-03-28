package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"github.com/lucas-passera/chat-server/server-pack/src/main/entities"
	"github.com/lucas-passera/chat-server/server-pack/src/main/service"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

var connections = make(map[*websocket.Conn]bool) //Active connections map
var mu sync.Mutex

// Handler WebSocket
func ChatHandler(c *gin.Context) {

	conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)

	if err != nil {
		log.Println("Error upgrading connection:", err)
		return
	}

	defer func() {
		// Remove connection from map when closed
		mu.Lock()
		delete(connections, conn)
		mu.Unlock()
		conn.Close()
		log.Println("Client disconnected")
	}()

	mu.Lock()
	connections[conn] = true
	mu.Unlock()

	log.Println("New client connected")

	messageService := service.NewMessageService()

	for {
		_, msg, err := conn.ReadMessage()

		if err != nil {
			log.Println("Error reading message:", err)
			break
		}
		log.Println("Message received:", string(msg))

		var message entities.Message
		err = json.Unmarshal(msg, &message)

		if err != nil {
			log.Println("Error parsing the message:", err)
			continue
		}

		if err := messageService.CreateMessage(&message); err != nil {
			log.Println("Error saving message:", err)
		} else {
			log.Printf("Message saved: (ID-%d) UserID-%d: %s (%s)", message.ID, message.UserID, message.Content, message.CreatedAt)
		}

		// Broadcast the message to all active clients
		mu.Lock()
		for c := range connections {
			if err := c.WriteMessage(websocket.TextMessage, []byte(msg)); err != nil {
				log.Println("Error sending message:", err)
				// If there's an error sending a message, remove this client
				c.Close()
				delete(connections, c)
			}
		}
		mu.Unlock()
	}

}
