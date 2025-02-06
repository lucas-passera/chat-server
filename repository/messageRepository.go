package repository

import (
	"errors"

	"github.com/lucas-passera/chat-server/database"
	"github.com/lucas-passera/chat-server/entities"
)

// CreateMessage guarda un nuevo mensaje en la base de datos
func CreateMessage(msg *entities.Message) error {
	return database.DB.Create(msg).Error
}

// GetMessageByID obtiene un mensaje por su ID
func GetMessageByID(id uint) (*entities.Message, error) {
	var msg entities.Message
	err := database.DB.First(&msg, id).Error
	if err != nil {
		return nil, errors.New("mensaje no encontrado")
	}
	return &msg, nil
}

// GetMessagesByUserID obtiene todos los mensajes enviados por un usuario
func GetMessagesByUserID(userID uint) ([]entities.Message, error) {
	var messages []entities.Message
	err := database.DB.Where("user_id = ?", userID).Find(&messages).Error
	if err != nil {
		return nil, errors.New("no se encontraron mensajes")
	}
	return messages, nil
}

// GetAllMessages obtiene todos los mensajes
func GetAllMessages() ([]entities.Message, error) {
	var messages []entities.Message
	err := database.DB.Find(&messages).Error
	if err != nil {
		return nil, errors.New("no se encontraron mensajes")
	}
	return messages, nil
}

// UpdateMessage actualiza los datos de un mensaje
func UpdateMessage(msg *entities.Message) error {
	return database.DB.Save(msg).Error
}

// DeleteMessage elimina un mensaje por su ID
func DeleteMessage(id uint) error {
	var msg entities.Message
	err := database.DB.First(&msg, id).Error
	if err != nil {
		return errors.New("mensaje no encontrado")
	}
	return database.DB.Delete(&msg).Error
}
