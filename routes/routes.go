package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/lucas-passera/chat-server/handlers"
)

func SetupRoutes(router *gin.Engine) {
	// Rutas de usuario
	router.POST("/users", handlers.CreateUser)
	router.GET("/users", handlers.GetAllUsers)
	router.PUT("/users", handlers.UpdateUser)
	router.DELETE("/users/:id", handlers.DeleteUser)

	// Rutas de mensajes
	router.POST("/messages", handlers.CreateMessage)
	router.GET("/messages", handlers.GetAllMessages)
	router.DELETE("/messages/:id", handlers.DeleteMessage)

	// Ruta WebSocket para el chat en tiempo real
	router.GET("/chat", handlers.ChatHandler)
}
