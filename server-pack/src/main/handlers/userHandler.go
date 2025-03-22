package handlers

import (
	"net/http"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/lucas-passera/chat-server/server-pack/src/main/entities"
	"github.com/lucas-passera/chat-server/server-pack/src/main/service"
)

func CreateUser(c *gin.Context) {

	var user entities.User

	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid data"})
		return
	}
	err := service.NewUserService().CreateUser(&user)
	if err != nil {
		if strings.Contains(err.Error(), "username already exists") {
			c.JSON(http.StatusConflict, gin.H{"error": "username already exists"}) // 409 Conflict
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not create the user"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "user created successfully", "user": user})
}

func GetUser(c *gin.Context) {

	idStr := c.Param("id")
	id, err := strconv.ParseUint(idStr, 10, 32)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid ID"})
		return
	}
	user, err := service.NewUserService().GetUserByID(uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"user": user})
}

func GetUserByUsername(c *gin.Context) {
	username := c.Param("username")
	user, err := service.NewUserService().GetUserByUsername(username)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"user": user})
}

func GetAllUsers(c *gin.Context) {

	users, err := service.NewUserService().GetAllUsers()

	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"users": users})
}

func UpdateUser(c *gin.Context) {

	var user entities.User

	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid data"})
		return
	}

	if err := service.NewUserService().UpdateUser(&user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not update the user"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "user updated successfully", "user": user})
}

func DeleteUser(c *gin.Context) {

	idStr := c.Param("id")
	id, err := strconv.ParseUint(idStr, 10, 32)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid ID"})
		return
	}

	if err := service.NewUserService().DeleteUser(uint(id)); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "user deleted successfully"})
}

func DeleteAllUsers(c *gin.Context) {

	if err := service.NewUserService().DeleteAllUsers(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Could not reset users"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "all users deleted, id reset to 1"})
}

func CheckUsernameHandler(c *gin.Context) {
	username := c.Param("username")
	userService := service.UserService{}
	exists, err := userService.CheckUsername(username)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not check username"})
		return
	}
	if exists {
		c.JSON(http.StatusConflict, gin.H{"message": "username already exists"})
		return
	} else {
		c.JSON(http.StatusOK, gin.H{"message": "username is available"})
		return
	}
}

func CheckUserPassword(c *gin.Context) {
	var userService = service.UserService{}
	var req struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Datos inválidos"})
		return
	}

	if userService.CheckUserPassword(req.Username, req.Password) {
		c.JSON(http.StatusOK, gin.H{"message": "✅ Contraseña correcta"})
	} else {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Usuario o contraseña incorrectos"})
	}
}
