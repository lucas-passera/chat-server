package database

import (
	"fmt"
	"log"

	"github.com/lucas-passera/chat-server/entities"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConnectDatabase() {
	//connection cfg
	//TODO NO PASS HERE
	dsn := "root:Lucaspassera19*@tcp(127.0.0.1:3306)/chatserver_db?charset=utf8mb4&parseTime=True&loc=Local"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})

	if err != nil {
		log.Fatal("Connection with database(ERROR):", err)
	}

	DB = db
	fmt.Println("MySQL Connection Successfully!")

	//orm
	err = DB.AutoMigrate(&entities.User{}, &entities.Message{})

	if err != nil {
		log.Fatal("Error migrating database:", err)
	}
	fmt.Println("Database migration successful!")
}
