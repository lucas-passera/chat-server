package service

import (
	"errors"
	"log"

	"github.com/lucas-passera/chat-server/entities"
	"github.com/lucas-passera/chat-server/repository"
)

type MessageService struct{}

func NewMessageService() *MessageService {
	return &MessageService{}
}

func (s *MessageService) CreateMessage(msg *entities.Message) error {
	if msg.UserID == 0 || msg.Content == "" {
		return errors.New("user ID and content are required")
	}
	return repository.CreateMessage(msg)
}

func (s *MessageService) GetMessageByID(id uint) (*entities.Message, error) {
	return repository.GetMessageByID(id)
}

func (s *MessageService) GetMessagesByUserID(userID uint) ([]entities.Message, error) {
	return repository.GetMessagesByUserID(userID)
}

func (s *MessageService) GetAllMessages() ([]entities.Message, error) {
	return repository.GetAllMessages()
}

func (s *MessageService) UpdateMessage(msg *entities.Message) error {
	if msg.ID == 0 {
		return errors.New("message ID is required")
	}
	return repository.UpdateMessage(msg)
}

func (s *MessageService) DeleteMessage(id uint) error {
	exists, err := repository.CheckMessageID(id)
	if err != nil {
		log.Println("Error checking if the message exists:", err)
		return err
	}
	if !exists {
		return errors.New("message not found")
	}
	return repository.DeleteMessage(id)
}

func (s *MessageService) DeleteAllMessages() error {
	return repository.DeleteAllMessages()
}
