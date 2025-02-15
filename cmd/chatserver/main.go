package main

import (
	"fmt"

	"github.com/gin-gonic/gin"
	"github.com/lucas-passera/chat-server/database"
	"github.com/lucas-passera/chat-server/routes"
)

func main() {

	database.ConnectDatabase()
	router := gin.Default()
	routes.SetupRoutes(router)
	fmt.Println("Chat Server App is running (PORT:8081)") //TODO cfg app
	router.Run(":8081")

}
