// Contact Page JavaScript
document.addEventListener("DOMContentLoaded", () => {
    // Form validation
    const contactForm = document.querySelector(".contact-form")
    if (contactForm) {
      contactForm.addEventListener("submit", (e) => {
        const name = document.getElementById("name").value.trim()
        const email = document.getElementById("email").value.trim()
        const message = document.getElementById("message").value.trim()
  
        if (!name || !email || !message) {
          e.preventDefault()
          alert("Please fill in all required fields.")
          return false
        }
  
        if (!isValidEmail(email)) {
          e.preventDefault()
          alert("Please enter a valid email address.")
          return false
        }
      })
    }
  
    // Email validation
    function isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(email)
    }
  
    // Phone number formatting
    const phoneInput = document.getElementById("phone")
    if (phoneInput) {
      phoneInput.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "")
        if (value.length >= 6) {
          value = value.replace(/(\d{3})(\d{3})(\d{4})/, "($1) $2-$3")
        } else if (value.length >= 3) {
          value = value.replace(/(\d{3})(\d{3})/, "($1) $2")
        }
        e.target.value = value
      })
    }
  })
  