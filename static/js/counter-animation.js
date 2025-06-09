// Counter animation for statistics
document.addEventListener("DOMContentLoaded", () => {
  initCounterAnimations()
})

function initCounterAnimations() {
  const counters = document.querySelectorAll(".stat-number[data-count]")

  const observerOptions = {
    threshold: 0.5,
    rootMargin: "0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCounter(entry.target)
        observer.unobserve(entry.target)
      }
    })
  }, observerOptions)

  counters.forEach((counter) => {
    observer.observe(counter)
  })
}

function animateCounter(element) {
  const target = Number.parseInt(element.getAttribute("data-count"))
  const duration = 2000 // 2 seconds
  const increment = target / (duration / 16) // 60fps
  let current = 0

  const timer = setInterval(() => {
    current += increment

    if (current >= target) {
      current = target
      clearInterval(timer)
    }

    // Format number with commas
    element.textContent = Math.floor(current).toLocaleString()
  }, 16)

  // Add animation class for additional effects
  element.classList.add("counting")

  setTimeout(() => {
    element.classList.remove("counting")
  }, duration)
}

// CSS for counting animation
const style = document.createElement("style")
style.textContent = `
    .stat-number.counting {
        transform: scale(1.1);
        transition: transform 0.3s ease;
    }
    
    .stat-number {
        transition: transform 0.3s ease;
    }
`
document.head.appendChild(style)
