package main

import (
	"fmt"

	"github.com/lucas-passera/chat-server/server-pack/src/main/database"

	"github.com/lucas-passera/chat-server/server-pack/src/main/routes"

	"github.com/gin-gonic/gin"
)

func main() {

	database.ConnectDatabase()
	router := gin.Default()
	routes.SetupRoutes(router)
	fmt.Println("Chat Server App is running (PORT:8081)") //TODO cfg app
	router.Run(":8081")

}
