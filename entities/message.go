package entities

import (
	"gorm.io/gorm"
)

type Message struct {
	gorm.Model
	UserID  uint   `json:"user_id"`
	Content string `json:"content"`
}
