package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/lucas-passera/chat-server/entities"
	"github.com/lucas-passera/chat-server/repository"
)

// CreateMessage guarda un nuevo mensaje
func CreateMessage(c *gin.Context) {
	var msg entities.Message
	if err := c.ShouldBindJSON(&msg); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "datos inválidos"})
		return
	}

	// Usar el repositorio para guardar el mensaje
	if err := repository.CreateMessage(&msg); err != nil {
		// Si el error contiene "duplicate key" o similar, lo tratamos como conflicto
		if err.Error() == "duplicate key value violates unique constraint" {
			c.JSON(http.StatusConflict, gin.H{"error": "mensaje duplicado"})
			return
		}
		// Otro tipo de errores generales
		c.JSON(http.StatusInternalServerError, gin.H{"error": "no se pudo crear el mensaje"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "mensaje creado correctamente", "messages": msg})
}

// GetMessage obtiene un mensaje por su ID
func GetMessage(c *gin.Context) {
	idStr := c.Param("id")

	// Convertir el id a uint
	id, err := strconv.ParseUint(idStr, 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
		return
	}

	msg, err := repository.GetMessageByID(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": msg})
}

// GetMessagesByUser obtiene todos los mensajes enviados por un usuario
func GetMessagesByUser(c *gin.Context) {
	userIDStr := c.Param("user_id")

	// Convertir el userID a uint
	userID, err := strconv.ParseUint(userIDStr, 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "ID de usuario inválido"})
		return
	}

	messages, err := repository.GetMessagesByUserID(uint(userID))
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"messages": messages})
}

// GetAllMessages obtiene todos los mensajes
func GetAllMessages(c *gin.Context) {
	messages, err := repository.GetAllMessages()
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"messages": messages})
}

// UpdateMessage actualiza un mensaje existente
func UpdateMessage(c *gin.Context) {
	var msg entities.Message
	if err := c.ShouldBindJSON(&msg); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "datos inválidos"})
		return
	}

	// Usar el repositorio para actualizar el mensaje
	if err := repository.UpdateMessage(&msg); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "no se pudo actualizar el mensaje"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "mensaje actualizado correctamente", "messages": msg})
}

// DeleteMessage elimina un mensaje por su ID
func DeleteMessage(c *gin.Context) {
	idStr := c.Param("id")

	// Convertir el id a uint
	id, err := strconv.ParseUint(idStr, 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
		return
	}

	// Usar el repositorio para eliminar el mensaje
	if err := repository.DeleteMessage(uint(id)); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "mensaje eliminado correctamente"})
}
