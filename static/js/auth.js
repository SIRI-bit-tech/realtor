// Authentication JavaScript
document.addEventListener("DOMContentLoaded", () => {
    // Password strength indicator
    const passwordInput = document.getElementById("id_password1")
    if (passwordInput) {
      passwordInput.addEventListener("input", function () {
        checkPasswordStrength(this.value)
      })
    }
  
    function checkPasswordStrength(password) {
      const strengthIndicator = document.getElementById("password-strength")
      if (!strengthIndicator) return
  
      let strength = 0
      const checks = [
        password.length >= 8,
        /[a-z]/.test(password),
        /[A-Z]/.test(password),
        /\d/.test(password),
        /[^a-zA-Z\d]/.test(password),
      ]
  
      strength = checks.filter((check) => check).length
  
      const strengthLevels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
      const strengthColors = ["#dc3545", "#fd7e14", "#ffc107", "#20c997", "#28a745"]
  
      strengthIndicator.textContent = strengthLevels[strength - 1] || ""
      strengthIndicator.style.color = strengthColors[strength - 1] || "#6c757d"
    }
  
    // Form validation
    const authForms = document.querySelectorAll(".auth-form")
    authForms.forEach((form) => {
      form.addEventListener("submit", (e) => {
        const requiredFields = form.querySelectorAll("[required]")
        let isValid = true
  
        requiredFields.forEach((field) => {
          if (!field.value.trim()) {
            isValid = false
            field.classList.add("is-invalid")
          } else {
            field.classList.remove("is-invalid")
          }
        })
  
        if (!isValid) {
          e.preventDefault()
          showAlert("Please fill in all required fields.", "error")
        }
      })
    })
  
    // Show alert function
    function showAlert(message, type = "info") {
      const alertContainer = document.getElementById("auth-messages")
      if (!alertContainer) return
  
      const alert = document.createElement("div")
      alert.className = `alert alert-${type}`
      alert.textContent = message
  
      alertContainer.innerHTML = ""
      alertContainer.appendChild(alert)
  
      setTimeout(() => {
        alert.remove()
      }, 5000)
    }
  
    // Toggle password visibility
    const passwordToggles = document.querySelectorAll(".password-toggle")
    passwordToggles.forEach((toggle) => {
      toggle.addEventListener("click", function () {
        const input = this.previousElementSibling
        const type = input.getAttribute("type") === "password" ? "text" : "password"
        input.setAttribute("type", type)
  
        const icon = this.querySelector("i")
        icon.classList.toggle("fa-eye")
        icon.classList.toggle("fa-eye-slash")
      })
    })
  })
  