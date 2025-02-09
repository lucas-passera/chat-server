package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"github.com/lucas-passera/chat-server/entities"
	"github.com/lucas-passera/chat-server/service"
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
	defer conn.Close()
	mu.Lock()
	connections[conn] = true
	mu.Unlock()

	log.Println("New client connected")

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

		if err := service.NewMessageService().CreateMessage(&message); err != nil {
			log.Println("Error saving message:", err)
		} else {
			log.Printf("Message saved: (ID-%d) UserID-%d: %s (%s)", message.ID, message.UserID, message.Content, message.CreatedAt)
		}

		mu.Lock()
		for c := range connections {
			if err := c.WriteMessage(websocket.TextMessage, []byte(msg)); err != nil {
				log.Println("Error sending message", err)
			}
		}
		mu.Unlock()
	}

}
