package database

import (
	"fmt"
	"log"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConnectDatabase() {
	// Establece la cadena de conexión con el servidor MySQL y la base de datos 'pets_db'
	dsn := "root:Lucaspassera19*@tcp(localhost:3306)/chatserver_db?charset=utf8mb4&parseTime=True&loc=Local"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Connection with database(ERROR):", err)
	}

	DB = db
	fmt.Println("MySQL Connection Successfully!")

	//Ejecuta la migración para las tablas 'Pet' y 'User'
	err = DB.AutoMigrate(&entities.User{}, &entities.Message{})
	if err != nil {
		log.Fatal("Error migrating database:", err)
	}
	fmt.Println("Database migration successful!")
}
