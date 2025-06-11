// Messaging functionality
document.addEventListener("DOMContentLoaded", () => {
    // Auto-scroll to bottom of messages
    const messagesContainer = document.getElementById("messages-container")
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight
    }
  
    // Handle message form submission
    const messageForm = document.querySelector(".message-form")
    if (messageForm) {
      messageForm.addEventListener("htmx:afterRequest", (event) => {
        if (event.detail.successful) {
          // Clear the form
          const textarea = messageForm.querySelector("textarea")
          if (textarea) {
            textarea.value = ""
          }
  
          // Scroll to bottom
          setTimeout(() => {
            if (messagesContainer) {
              messagesContainer.scrollTop = messagesContainer.scrollHeight
            }
          }, 100)
        }
      })
    }
  
    // Auto-resize textarea
    const messageInput = document.querySelector(".message-input")
    if (messageInput) {
      messageInput.addEventListener("input", function () {
        this.style.height = "auto"
        this.style.height = Math.min(this.scrollHeight, 120) + "px"
      })
  
      // Submit on Ctrl+Enter
      messageInput.addEventListener("keydown", (e) => {
        if (e.ctrlKey && e.key === "Enter") {
          e.preventDefault()
          messageForm.dispatchEvent(new Event("submit"))
        }
      })
    }
  
    // Mark messages as read when viewing conversation
    const conversationPage = document.querySelector(".conversation-page")
    if (conversationPage) {
      // Mark as read after a short delay
      setTimeout(() => {
        const conversationId = window.location.pathname.split("/").slice(-2, -1)[0]
        if (conversationId) {
          fetch(`/messaging/conversations/${conversationId}/mark-read/`, {
            method: "POST",
            headers: {
              "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
              "Content-Type": "application/json",
            },
          })
        }
      }, 1000)
    }
  })
  
  // Global function for scrolling to bottom
  function scrollToBottom() {
    const container = document.getElementById("messages-container")
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  }
  
  // Notification sound (optional)
  function playNotificationSound() {
    // You can add a notification sound here
    // const audio = new Audio('/static/sounds/notification.mp3');
    // audio.play().catch(() => {}); // Ignore errors if sound fails
  }
  