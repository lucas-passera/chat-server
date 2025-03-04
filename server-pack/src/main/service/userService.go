package service

import (
	"errors"
	"log"

	"github.com/lucas-passera/chat-server/entities"
	"github.com/lucas-passera/chat-server/repository"
	"golang.org/x/crypto/bcrypt"
)

type UserService struct{}

func NewUserService() *UserService {
	return &UserService{}
}

func (s *UserService) CreateUser(user *entities.User) error {

	if user.Username == "" {
		return errors.New("username is required")
	}

	if user.Password == "" {
		return errors.New("password is required")
	}

	if len(user.Password) > 15 {
		return errors.New("password must be at most 15 characters long")
	}

	exists, err := repository.CheckUsername(user.Username)
	if err != nil {
		return err
	}
	if exists {
		return errors.New("username already exists")
	}

	hashedPassword, err := hashPassword(user.Password)
	if err != nil {
		return errors.New("could not hash password")
	}

	user.Password = hashedPassword
	err = repository.CreateUser(user)
	if err != nil {
		return err
	}

	log.Println("UserService: User created successfully!")
	return nil
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

func hashPassword(password string) (string, error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	return string(bytes), err
}

func (s *UserService) CheckUserPassword(username, password string) bool {
	user, err := s.GetUserByUsername(username)
	if err != nil {
		return false
	}
	return checkPassword(user.Password, password)
}

func checkPassword(hashedPassword, password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
	return err == nil
}

func (s *UserService) DeleteAllUsers() error {
	return repository.DeleteAllUsers()
}

func (s *UserService) CheckUsername(username string) (bool, error) {
	exists, err := repository.CheckUsername(username)
	if err != nil {
		return false, err
	}
	return exists, nil
}
