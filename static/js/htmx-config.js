// HTMX Configuration and Extensions
document.addEventListener("DOMContentLoaded", () => {
  // Configure HTMX
  htmx.config.globalViewTransitions = true
  htmx.config.scrollBehavior = "smooth"

  // Add loading indicators
  document.body.addEventListener("htmx:beforeRequest", (evt) => {
    const target = evt.detail.target
    const indicator =
      target.querySelector(".htmx-indicator") || document.querySelector(`#${target.getAttribute("hx-indicator")}`)

    if (indicator) {
      indicator.style.display = "block"
    }

    // Add loading class to target
    target.classList.add("htmx-loading")
  })

  document.body.addEventListener("htmx:afterRequest", (evt) => {
    const target = evt.detail.target
    const indicator =
      target.querySelector(".htmx-indicator") || document.querySelector(`#${target.getAttribute("hx-indicator")}`)

    if (indicator) {
      indicator.style.display = "none"
    }

    // Remove loading class
    target.classList.remove("htmx-loading")
  })

  // Handle errors
  document.body.addEventListener("htmx:responseError", (evt) => {
    console.error("HTMX Error:", evt.detail)
    showNotification("An error occurred. Please try again.", "error")
  })

  // Handle successful swaps
  document.body.addEventListener("htmx:afterSwap", (evt) => {
    // Reinitialize components after HTMX swap
    initializeComponents(evt.detail.target)
  })

  // HTMX global CSRF handler for Django
  // Ensures all HTMX POST requests include the CSRF token

  document.body.addEventListener('htmx:configRequest', function(event) {
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    event.detail.headers['X-CSRFToken'] = getCookie('csrftoken');
  });
})

// Initialize components after HTMX swaps
function initializeComponents(container = document) {
  // Reinitialize dropdowns
  initDropdowns(container)

  // Reinitialize tooltips
  initTooltips(container)

  // Reinitialize modals
  initModals(container)

  // Reinitialize form validation
  initFormValidation(container)
}

function initDropdowns(container) {
  const dropdowns = container.querySelectorAll(".dropdown")

  dropdowns.forEach((dropdown) => {
    const toggle = dropdown.querySelector(".dropdown-toggle")
    const menu = dropdown.querySelector(".dropdown-menu")

    if (toggle && menu) {
      toggle.addEventListener("click", (e) => {
        e.stopPropagation()

        // Close other dropdowns
        document.querySelectorAll(".dropdown-menu.show").forEach((otherMenu) => {
          if (otherMenu !== menu) {
            otherMenu.classList.remove("show")
          }
        })

        menu.classList.toggle("show")
      })
    }
  })

  // Close dropdowns when clicking outside
  document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown-menu.show").forEach((menu) => {
      menu.classList.remove("show")
    })
  })
}

function initTooltips(container) {
  const tooltips = container.querySelectorAll("[data-tooltip]")

  tooltips.forEach((element) => {
    const text = element.getAttribute("data-tooltip")
    const position = element.getAttribute("data-tooltip-position") || "top"

    const tooltip = document.createElement("div")
    tooltip.className = `tooltip-content tooltip-${position}`
    tooltip.textContent = text

    element.style.position = "relative"
    element.appendChild(tooltip)
  })
}

function initModals(container) {
  const modalTriggers = container.querySelectorAll("[data-modal]")

  modalTriggers.forEach((trigger) => {
    const modalId = trigger.getAttribute("data-modal")
    const modal = document.getElementById(modalId)

    if (modal) {
      trigger.addEventListener("click", (e) => {
        e.preventDefault()
        openModal(modal)
      })
    }
  })

  // Close modal handlers
  const closeButtons = container.querySelectorAll("[data-modal-close]")
  closeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const modal = button.closest(".modal-dialog")
      if (modal) {
        closeModal(modal)
      }
    })
  })
}

function openModal(modal) {
  const backdrop = modal.querySelector(".modal-backdrop") || modal.parentElement.querySelector(".modal-backdrop")

  if (backdrop) {
    backdrop.classList.add("show")
  }
  modal.classList.add("show")
  document.body.style.overflow = "hidden"
}

function closeModal(modal) {
  const backdrop = modal.querySelector(".modal-backdrop") || modal.parentElement.querySelector(".modal-backdrop")

  if (backdrop) {
    backdrop.classList.remove("show")
  }
  modal.classList.remove("show")
  document.body.style.overflow = ""
}

function initFormValidation(container) {
  const forms = container.querySelectorAll("form[data-validate]")

  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!validateForm(form)) {
        e.preventDefault()
      }
    })

    // Real-time validation
    const inputs = form.querySelectorAll("input, textarea, select")
    inputs.forEach((input) => {
      input.addEventListener("blur", () => {
        validateField(input)
      })
    })
  })
}

function validateForm(form) {
  let isValid = true
  const inputs = form.querySelectorAll("input[required], textarea[required], select[required]")

  inputs.forEach((input) => {
    if (!validateField(input)) {
      isValid = false
    }
  })

  return isValid
}

function validateField(field) {
  const value = field.value.trim()
  const type = field.type
  let isValid = true
  let message = ""

  // Required validation
  if (field.hasAttribute("required") && !value) {
    isValid = false
    message = "This field is required"
  }

  // Email validation
  if (type === "email" && value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      isValid = false
      message = "Please enter a valid email address"
    }
  }

  // Phone validation
  if (type === "tel" && value) {
    const phoneRegex = /^[+]?[1-9][\d]{0,15}$/
    if (!phoneRegex.test(value.replace(/[\s\-$$$$]/g, ""))) {
      isValid = false
      message = "Please enter a valid phone number"
    }
  }

  // Update field appearance
  field.classList.toggle("error", !isValid)

  // Show/hide error message
  let errorElement = field.parentElement.querySelector(".form-error")
  if (!isValid && message) {
    if (!errorElement) {
      errorElement = document.createElement("div")
      errorElement.className = "form-error"
      field.parentElement.appendChild(errorElement)
    }
    errorElement.textContent = message
  } else if (errorElement) {
    errorElement.remove()
  }

  return isValid
}

// Utility function for notifications (if not already defined)
if (typeof showNotification === "undefined") {
  function showNotification(message, type = "info") {
    const notification = document.createElement("div")
    notification.className = `notification notification-${type}`
    notification.innerHTML = `
            <i class="icon-${type === "error" ? "x" : type === "success" ? "check" : "info"}"></i>
            <span>${message}</span>
        `

    // Style the notification
    Object.assign(notification.style, {
      position: "fixed",
      top: "20px",
      right: "20px",
      padding: "15px 20px",
      borderRadius: "8px",
      color: "white",
      fontWeight: "600",
      zIndex: "10000",
      transform: "translateX(100%)",
      transition: "transform 0.3s ease-in-out",
      display: "flex",
      alignItems: "center",
      gap: "10px",
    })

    // Set background color based on type
    const colors = {
      success: "#10b981",
      error: "#ef4444",
      warning: "#f59e0b",
      info: "#3b82f6",
    }
    notification.style.backgroundColor = colors[type] || colors.info

    document.body.appendChild(notification)

    // Animate in
    setTimeout(() => {
      notification.style.transform = "translateX(0)"
    }, 100)

    // Remove after 5 seconds
    setTimeout(() => {
      notification.style.transform = "translateX(100%)"
      setTimeout(() => {
        if (document.body.contains(notification)) {
          document.body.removeChild(notification)
        }
      }, 300)
    }, 5000)
  }
}

// Initialize components on page load
document.addEventListener("DOMContentLoaded", () => {
  initializeComponents()
})
