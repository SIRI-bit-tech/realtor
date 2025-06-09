// About Page JavaScript
document.addEventListener("DOMContentLoaded", () => {
    // Animate statistics on scroll
    const observerOptions = {
      threshold: 0.5,
      rootMargin: "0px 0px -50px 0px",
    }
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateStats()
          observer.unobserve(entry.target)
        }
      })
    }, observerOptions)
  
    const statsSection = document.querySelector(".story-stats")
    if (statsSection) {
      observer.observe(statsSection)
    }
  
    function animateStats() {
      const statNumbers = document.querySelectorAll(".stat-item h3")
  
      statNumbers.forEach((stat) => {
        const finalNumber = Number.parseInt(stat.textContent.replace(/\D/g, ""))
        const suffix = stat.textContent.replace(/\d/g, "")
        let currentNumber = 0
        const increment = finalNumber / 50
  
        const timer = setInterval(() => {
          currentNumber += increment
          if (currentNumber >= finalNumber) {
            stat.textContent = finalNumber + suffix
            clearInterval(timer)
          } else {
            stat.textContent = Math.floor(currentNumber) + suffix
          }
        }, 30)
      })
    }
  
    // Team card hover effects
    const teamCards = document.querySelectorAll(".team-card")
    teamCards.forEach((card) => {
      card.addEventListener("mouseenter", function () {
        this.style.transform = "translateY(-10px)"
      })
  
      card.addEventListener("mouseleave", function () {
        this.style.transform = "translateY(0)"
      })
    })
  
    // Value cards animation
    const valueCards = document.querySelectorAll(".value-card")
    const valueObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, index) => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              entry.target.style.opacity = "1"
              entry.target.style.transform = "translateY(0)"
            }, index * 200)
          }
        })
      },
      { threshold: 0.3 },
    )
  
    valueCards.forEach((card) => {
      card.style.opacity = "0"
      card.style.transform = "translateY(30px)"
      card.style.transition = "all 0.6s ease"
      valueObserver.observe(card)
    })
  })
  