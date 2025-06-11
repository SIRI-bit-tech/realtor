// Main JavaScript functionality
document.addEventListener("DOMContentLoaded", () => {
  // Initialize all components
  initNavigation()
  initUserMenu()
  initLoadingScreen()
  initScrollEffects()
  initMobileMenu()

  // HTMX configuration
  configureHTMX()
})

// Navigation functionality
function initNavigation() {
  const navbar = document.getElementById("navbar")
  let lastScrollY = window.scrollY

  window.addEventListener("scroll", () => {
    const currentScrollY = window.scrollY

    // Add scrolled class for styling
    if (currentScrollY > 50) {
      navbar.classList.add("scrolled")
    } else {
      navbar.classList.remove("scrolled")
    }

    // Hide/show navbar on scroll
    if (currentScrollY > lastScrollY && currentScrollY > 100) {
      navbar.style.transform = "translateY(-100%)"
    } else {
      navbar.style.transform = "translateY(0)"
    }

    lastScrollY = currentScrollY
  })
}

// User menu dropdown
function initUserMenu() {
  const userMenuToggle = document.getElementById("user-menu-toggle")
  const userDropdown = document.getElementById("user-dropdown")

  if (userMenuToggle && userDropdown) {
    userMenuToggle.addEventListener("click", (e) => {
      e.stopPropagation()
      userDropdown.classList.toggle("show")
    })

    // Close dropdown when clicking outside
    document.addEventListener("click", (e) => {
      if (!userMenuToggle.contains(e.target)) {
        userDropdown.classList.remove("show")
      }
    })
  }
}

// Loading screen
function initLoadingScreen() {
  const loadingScreen = document.getElementById("loading-screen")

  window.addEventListener("load", () => {
    setTimeout(() => {
      loadingScreen.classList.add("hidden")
    }, 500)
  })
}

// Scroll effects and animations
function initScrollEffects() {
  // Intersection Observer for fade-in animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible")
      }
    })
  }, observerOptions)

  // Observe all elements with fade-in class
  document.querySelectorAll(".fade-in, [data-aos]").forEach((el) => {
    observer.observe(el)
  })
}

// Mobile menu
function initMobileMenu() {
  const navToggle = document.getElementById("nav-toggle")
  const navMenu = document.getElementById("nav-menu")

  if (navToggle && navMenu) {
    // Fix: Properly toggle mobile menu
    navToggle.addEventListener("click", (e) => {
      e.preventDefault()
      e.stopPropagation()
      navToggle.classList.toggle("active")
      navMenu.classList.toggle("show")

      // Add visible class to ensure it displays
      if (navMenu.classList.contains("show")) {
        navMenu.style.display = "block"
        // Animate in
        setTimeout(() => {
          navMenu.style.transform = "translateY(0)"
          navMenu.style.opacity = "1"
        }, 10)
      } else {
        // Animate out
        navMenu.style.transform = "translateY(-10px)"
        navMenu.style.opacity = "0"
        setTimeout(() => {
          navMenu.style.display = "none"
        }, 300)
      }
    })

    // Close menu when clicking on links
    navMenu.querySelectorAll(".nav-link").forEach((link) => {
      link.addEventListener("click", () => {
        navToggle.classList.remove("active")
        navMenu.classList.remove("show")
        navMenu.style.transform = "translateY(-10px)"
        navMenu.style.opacity = "0"
        setTimeout(() => {
          navMenu.style.display = "none"
        }, 300)
      })
    })

    // Close when clicking outside
    document.addEventListener("click", (e) => {
      if (navMenu.classList.contains("show") && !navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navToggle.classList.remove("active")
        navMenu.classList.remove("show")
        navMenu.style.transform = "translateY(-10px)"
        navMenu.style.opacity = "0"
        setTimeout(() => {
          navMenu.style.display = "none"
        }, 300)
      }
    })
  }
}

// HTMX configuration
function configureHTMX() {
  // Add loading indicators
  document.body.addEventListener("htmx:beforeRequest", (evt) => {
    const indicator = evt.detail.elt.querySelector(".htmx-indicator")
    if (indicator) {
      indicator.style.display = "block"
    }
  })

  document.body.addEventListener("htmx:afterRequest", (evt) => {
    const indicator = evt.detail.elt.querySelector(".htmx-indicator")
    if (indicator) {
      indicator.style.display = "none"
    }
  })

  // Handle form submissions
  document.body.addEventListener("htmx:responseError", (evt) => {
    console.error("HTMX Error:", evt.detail)
    showNotification("An error occurred. Please try again.", "error")
  })

  // Success notifications
  document.body.addEventListener("htmx:afterSwap", (evt) => {
    if (evt.detail.target.classList.contains("success-message")) {
      showNotification("Action completed successfully!", "success")
    }
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
}

// Utility functions
function showNotification(message, type = "info") {
  const notification = document.createElement("div")
  notification.className = `notification notification-${type}`
  notification.textContent = message

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
      document.body.removeChild(notification)
    }, 300)
  }, 5000)
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  })
})

// Debounce function for performance
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Throttle function for scroll events
function throttle(func, limit) {
  let inThrottle
  return function () {
    const args = arguments

    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}
