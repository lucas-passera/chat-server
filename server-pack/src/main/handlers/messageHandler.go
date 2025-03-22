package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/lucas-passera/chat-server/server-pack/src/main/entities"
	"github.com/lucas-passera/chat-server/server-pack/src/main/service"
)

func CreateMessage(c *gin.Context) {

	var msg entities.Message
	if err := c.ShouldBindJSON(&msg); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid data."})
		return
	}

	if err := service.NewMessageService().CreateMessage(&msg); err != nil {

		if err.Error() == "duplicate key value violates unique constraint" {
			c.JSON(http.StatusConflict, gin.H{"error": "duplicate id message."})
			return
		}

		c.JSON(http.StatusInternalServerError, gin.H{"error": "the message could not be created."})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "message create successfully", "messages": msg})
}

func GetMessage(c *gin.Context) {

	idStr := c.Param("id")
	id, err := strconv.ParseUint(idStr, 10, 32)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid ID."})
		return
	}

	msg, err := service.NewMessageService().GetMessageByID(uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": msg})
}

func GetMessagesByUser(c *gin.Context) {

	userIDStr := c.Param("user_id")
	userID, err := strconv.ParseUint(userIDStr, 10, 32)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid user id."})
		return
	}

	messages, err := service.NewMessageService().GetMessagesByUserID(uint(userID))

	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"messages": messages})
}

func GetAllMessages(c *gin.Context) {

	messages, err := service.NewMessageService().GetAllMessages()

	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"messages": messages})
}

func UpdateMessage(c *gin.Context) {

	var msg entities.Message

	if err := c.ShouldBindJSON(&msg); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid data."})
		return
	}

	if err := service.NewMessageService().UpdateMessage(&msg); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "The message could not be updated"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "message updated successfully", "messages": msg})
}

func DeleteMessage(c *gin.Context) {

	idStr := c.Param("id")
	id, err := strconv.ParseUint(idStr, 10, 32)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid id."})
		return
	}

	if err := service.NewMessageService().DeleteMessage(uint(id)); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "message delete successfully."})
}

func DeleteAllMessages(c *gin.Context) {

	if err := service.NewMessageService().DeleteAllMessages(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Could not reset messages"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "All messages deleted, ID reset to 1"})
}
