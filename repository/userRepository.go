package repository

import (
	"database/sql"
	"errors"
	"log"

	"github.com/lucas-passera/chat-server/database"
	"github.com/lucas-passera/chat-server/entities"
)

// CreateUser guarda un nuevo usuario en la base de datos
func CreateUser(user *entities.User) error {
	return database.DB.Create(user).Error
}

// GetUserByID obtiene un usuario por su ID
func GetUserByID(id uint) (*entities.User, error) {
	var user entities.User
	err := database.DB.First(&user, id).Error
	if err != nil {
		return nil, errors.New("usuario no encontrado")
	}
	return &user, nil
}

// GetUserByUsername obtiene un usuario por su nombre de usuario
func GetUserByUsername(username string) (*entities.User, error) {
	var user entities.User
	err := database.DB.Where("username = ?", username).First(&user).Error
	if err != nil {
		return nil, errors.New("usuario no encontrado")
	}
	return &user, nil
}

// GetAllUsers obtiene todos los usuarios
func GetAllUsers() ([]entities.User, error) {
	var users []entities.User
	err := database.DB.Find(&users).Error
	if err != nil {
		return nil, errors.New("no se encontraron usuarios")
	}
	return users, nil
}

// UpdateUser actualiza los datos de un usuario
func UpdateUser(user *entities.User) error {
	return database.DB.Save(user).Error
}

// DeleteUser elimina un usuario por su ID
func DeleteUser(id uint) error {
	var user entities.User
	err := database.DB.First(&user, id).Error
	if err != nil {
		return errors.New("usuario no encontrado")
	}
	return database.DB.Delete(&user).Error
}

var db *sql.DB

func CheckUserID(userID string) (bool, error) {
	var exists bool
	query := "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = ?)"
	err := db.QueryRow(query, userID).Scan(&exists)
	if err != nil {
		log.Println("Error al consultar el usuario:", err)
		return false, err
	}
	return exists, nil
}
