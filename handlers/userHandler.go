package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/lucas-passera/chat-server/entities"
	"github.com/lucas-passera/chat-server/repository"
)

// CreateUser crea un nuevo usuario
func CreateUser(c *gin.Context) {
	var user entities.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "datos inválidos"})
		return
	}

	// Usar el repositorio para guardar el usuario
	if err := repository.CreateUser(&user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "no se pudo crear el usuario"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "usuario creado correctamente", "user": user})
}

// GetUser obtiene un usuario por su ID
func GetUser(c *gin.Context) {
	// Obtener el parámetro 'id' de la URL como string
	idStr := c.Param("id")
	// Convertir el ID de string a uint
	id, err := strconv.ParseUint(idStr, 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
		return
	}

	// Buscar el usuario usando el ID convertido
	user, err := repository.GetUserByID(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	// Responder con el usuario encontrado
	c.JSON(http.StatusOK, gin.H{"user": user})
}

// GetAllUsers obtiene todos los usuarios
func GetAllUsers(c *gin.Context) {
	users, err := repository.GetAllUsers()
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"users": users})
}

// UpdateUser actualiza un usuario existente
func UpdateUser(c *gin.Context) {
	var user entities.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "datos inválidos"})
		return
	}

	// Usar el repositorio para actualizar el usuario
	if err := repository.UpdateUser(&user); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "no se pudo actualizar el usuario"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "usuario actualizado correctamente", "user": user})
}

// DeleteUser elimina un usuario por su ID
func DeleteUser(c *gin.Context) {
	// Obtener el parámetro 'id' de la URL como string
	idStr := c.Param("id")

	// Convertir el ID de string a uint
	id, err := strconv.ParseUint(idStr, 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
		return
	}

	// Usar el repositorio para eliminar el usuario
	if err := repository.DeleteUser(uint(id)); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "usuario eliminado correctamente"})
}
