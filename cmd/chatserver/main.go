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
	fmt.Println("Servidor chat corriendo en el puerto 8081")
	router.Run(":8081")
	//	r := mux.NewRouter()

	////ping pong route
	//r.HandleFunc("/ping", handlers.PingPongHandler).Methods("GET")
	//
	//// Rutas para Pet
	//r.HandleFunc("/pets", handlers.CreatePet).Methods("POST")
	//r.HandleFunc("/pets/{id}", handlers.GetPetByID).Methods("GET")
	//r.HandleFunc("/pets/{id}", handlers.UpdatePet).Methods("PUT")
	//r.HandleFunc("/pets/{id}", handlers.DeletePet).Methods("DELETE")
	//
	//// Rutas para User
	//r.HandleFunc("/users", handlers.CreateUser).Methods("POST")
	//r.HandleFunc("/users/{id}", handlers.GetUserByID).Methods("GET")
	//r.HandleFunc("/users/{id}", handlers.UpdateUser).Methods("PUT")
	//r.HandleFunc("/users/{id}", handlers.DeleteUser).Methods("DELETE")
	//
	//log.Fatal(http.ListenAndServe(":8081", r))
	//
	//
	//
}
