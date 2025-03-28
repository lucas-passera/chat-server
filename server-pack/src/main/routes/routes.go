package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/lucas-passera/chat-server/server-pack/src/main/handlers"
)

func SetupRoutes(router *gin.Engine) {
	// User routes
	router.POST("/users", handlers.CreateUser)
	router.POST("/users/check-password", handlers.CheckUserPassword)
	router.GET("/users", handlers.GetAllUsers)
	router.GET("users/:id", handlers.GetUser)
	router.GET("/users/username/:username", handlers.GetUserByUsername)
	router.GET("/users/check-username/:username", handlers.CheckUsernameHandler)
	router.PUT("/users", handlers.UpdateUser)
	router.DELETE("/users/:id", handlers.DeleteUser)
	router.DELETE("/users/delete-users", handlers.DeleteAllUsers)
	//TODO deleteAll Accessible to admins only

	// Message routes
	router.POST("/messages", handlers.CreateMessage)
	router.GET("/messages", handlers.GetAllMessages)
	router.DELETE("/messages/:id", handlers.DeleteMessage)
	router.DELETE("messages/delete-messages", handlers.DeleteAllMessages)

	// WebSocket
	router.GET("/chat", handlers.ChatHandler)
}
