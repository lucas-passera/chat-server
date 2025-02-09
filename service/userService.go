package service

import (
	"errors"
	"log"

	"github.com/lucas-passera/chat-server/entities"
	"github.com/lucas-passera/chat-server/repository"
)

type UserService struct{}

func NewUserService() *UserService {
	return &UserService{}
}

func (s *UserService) CreateUser(user *entities.User) error {
	if user.Username == "" {
		return errors.New("username is required")
	}
	return repository.CreateUser(user)
}

func (s *UserService) GetUserByID(id uint) (*entities.User, error) {
	return repository.GetUserByID(id)
}

func (s *UserService) GetUserByUsername(username string) (*entities.User, error) {
	return repository.GetUserByUsername(username)
}

func (s *UserService) GetAllUsers() ([]entities.User, error) {
	return repository.GetAllUsers()
}

func (s *UserService) UpdateUser(user *entities.User) error {
	if user.ID == 0 {
		return errors.New("user ID is required")
	}
	return repository.UpdateUser(user)
}

func (s *UserService) DeleteUser(id uint) error {
	exists, err := repository.CheckUserID(id)
	if err != nil {
		log.Println("Error checking if the user exists:", err)
		return err
	}
	if !exists {
		return errors.New("user not found")
	}
	return repository.DeleteUser(id)
}
