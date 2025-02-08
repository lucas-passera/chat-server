package handlers

import (
	"encoding/json"
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
var msg string

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

		// 🔍 LOG PARA DEBUG: Verificar que se está recibiendo el mensaje
		log.Println("Mensaje recibido:", string(msg))

		var message entities.Message
		err = json.Unmarshal(msg, &message)
		if err != nil {
			log.Println("Error al parsear el mensaje:", err)
			continue
		}

		// Ahora puedes acceder al user_id
		userID := message.UserID
		log.Printf("Recibido mensaje de user_id: %d, contenido: %s", userID, message.Content)

		//userIDStr := strconv.FormatUint(uint64(message.UserID), 10)
		//
		//// Verifica si el usuario existe pasando el ID como string
		//existsUser, err := repository.CheckUserID(userIDStr) // Pasamos el userID convertido a string
		//if err != nil {
		//	log.Println("Error al verificar si el usuario existe:", err)
		//	return
		//}
		//
		//if existsUser {
		//	log.Printf("El usuario con ID %s existe", userIDStr)
		//} else {
		//	log.Printf("El usuario con ID %s NO existe", userIDStr)
		//}
		//
		// Guardar el mensaje en la base de datos

		// Guardar el mensaje en la base de datos
		if err := repository.CreateMessage(&message); err != nil {
			log.Println("Error guardando mensaje:", err)
		} else {
			log.Println("Mensaje guardado con éxito:", message)
		}

		// Reenviar el mensaje a todos los clientes conectados
		mu.Lock()
		for c := range connections {
			if err := c.WriteMessage(websocket.TextMessage, []byte(msg)); err != nil {
				log.Println("Error enviando mensaje:", err)
			}
		}
		mu.Unlock()
	}

}
