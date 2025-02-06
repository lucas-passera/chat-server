package entities

import "gorm.io/gorm"

type User struct {
	gorm.Model        //This is for extends common attributes like ID, CreatedAt....
	Username   string `gorm:"uniqueIndex"`
	Password   string
}
