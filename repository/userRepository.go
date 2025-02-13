package repository

import (
	"errors"
	"log"

	"github.com/lucas-passera/chat-server/database"
	"github.com/lucas-passera/chat-server/entities"
)

func CreateUser(user *entities.User) error {
	return database.DB.Create(user).Error
}

func GetUserByID(id uint) (*entities.User, error) {
	var user entities.User
	err := database.DB.First(&user, id).Error
	if err != nil {
		return nil, errors.New("user not found")
	}
	return &user, nil
}

func GetUserByUsername(username string) (*entities.User, error) {
	var user entities.User
	err := database.DB.Where("username = ?", username).First(&user).Error
	if err != nil {
		return nil, errors.New("user not found")
	}
	return &user, nil
}

func GetAllUsers() ([]entities.User, error) {
	var users []entities.User
	err := database.DB.Find(&users).Error
	if err != nil {
		return nil, errors.New("users not found")
	}
	return users, nil
}

func UpdateUser(user *entities.User) error {
	return database.DB.Save(user).Error
}

func DeleteUser(id uint) error {
	var user entities.User
	err := database.DB.First(&user, id).Error
	if err != nil {
		return errors.New("user not found")
	}
	return database.DB.Delete(&user).Error
}

func DeleteAllUsers() error {
	db := database.DB
	tx := db.Begin()

	if err := tx.Exec("DELETE FROM users").Error; err != nil {
		tx.Rollback()
		return err
	}

	if err := tx.Exec("ALTER TABLE users AUTO_INCREMENT = 1").Error; err != nil {
		tx.Rollback()
		return err
	}

	return tx.Commit().Error
}

func CheckUserID(userID uint) (bool, error) {
	var exists bool
	query := "SELECT EXISTS(SELECT 1 FROM users WHERE id = ?)"
	err := database.DB.Raw(query, userID).Scan(&exists).Error
	if err != nil {
		log.Println("Error querying the user", err)
		return false, err
	}
	return exists, nil
}
