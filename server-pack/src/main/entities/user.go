package entities

import "gorm.io/gorm"

type User struct {
	gorm.Model        //This is for extends common attributes like ID, CreatedAt....
	Username   string `gorm:"type:varchar(255);uniqueIndex" json:"username"`
	Password   string `gorm:"type:varchar(255)" json:"password"`
}
