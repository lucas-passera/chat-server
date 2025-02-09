package repository

import (
	"errors"

	"github.com/lucas-passera/chat-server/database"
	"github.com/lucas-passera/chat-server/entities"
)

func CreateMessage(msg *entities.Message) error {
	return database.DB.Create(msg).Error
}

func GetMessageByID(id uint) (*entities.Message, error) {
	var msg entities.Message
	err := database.DB.First(&msg, id).Error
	if err != nil {
		return nil, errors.New("No messages found")
	}
	return &msg, nil
}

func GetMessagesByUserID(userID uint) ([]entities.Message, error) {
	var messages []entities.Message
	err := database.DB.Where("user_id = ?", userID).Find(&messages).Error
	if err != nil {
		return nil, errors.New("No messages found")
	}
	return messages, nil
}

func GetAllMessages() ([]entities.Message, error) {
	var messages []entities.Message
	err := database.DB.Find(&messages).Error
	if err != nil {
		return nil, errors.New("No messages found")
	}
	return messages, nil
}

func UpdateMessage(msg *entities.Message) error {
	return database.DB.Save(msg).Error
}

func DeleteMessage(id uint) error {
	var msg entities.Message
	err := database.DB.First(&msg, id).Error
	if err != nil {
		return errors.New("message not found.")
	}
	return database.DB.Delete(&msg).Error
}

func CheckMessageID(messageID uint) (bool, error) {
	var exists bool
	query := "SELECT EXISTS(SELECT 1 FROM messages WHERE id = ?)"
	err := database.DB.Raw(query, messageID).Scan(&exists).Error
	if err != nil {
		return false, err
	}
	return exists, nil
}
