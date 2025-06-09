// Animation utilities and effects
document.addEventListener("DOMContentLoaded", () => {
  initScrollAnimations()
  initParallaxElements()
  initCounterAnimations()
  initHoverEffects()
})

// Scroll-triggered animations
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll("[data-aos]")

  if (animatedElements.length === 0) return

  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const element = entry.target
        const animation = element.getAttribute("data-aos")
        const delay = element.getAttribute("data-aos-delay") || 0

        setTimeout(() => {
          element.classList.add("aos-animate")
          triggerAnimation(element, animation)
        }, delay)

        observer.unobserve(element)
      }
    })
  }, observerOptions)

  animatedElements.forEach((element) => {
    observer.observe(element)
  })
}

function triggerAnimation(element, animation) {
  switch (animation) {
    case "fade-up":
      element.style.opacity = "1"
      element.style.transform = "translateY(0)"
      break
    case "fade-down":
      element.style.opacity = "1"
      element.style.transform = "translateY(0)"
      break
    case "fade-left":
      element.style.opacity = "1"
      element.style.transform = "translateX(0)"
      break
    case "fade-right":
      element.style.opacity = "1"
      element.style.transform = "translateX(0)"
      break
    case "zoom-in":
      element.style.opacity = "1"
      element.style.transform = "scale(1)"
      break
    case "flip-up":
      element.style.opacity = "1"
      element.style.transform = "rotateX(0)"
      break
    default:
      element.style.opacity = "1"
      element.style.transform = "none"
  }
}

// Parallax effects
function initParallaxElements() {
  const parallaxElements = document.querySelectorAll("[data-parallax]")

  if (parallaxElements.length === 0) return

  // Check if user prefers reduced motion
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches
  if (prefersReducedMotion) return

  function updateParallax() {
    const scrolled = window.pageYOffset

    parallaxElements.forEach((element) => {
      const speed = Number.parseFloat(element.getAttribute("data-parallax")) || 0.5
      const rect = element.getBoundingClientRect()
      const isVisible = rect.bottom >= 0 && rect.top <= window.innerHeight

      if (isVisible) {
        const yPos = -(scrolled * speed)
        element.style.transform = `translateY(${yPos}px)`
      }
    })
  }

  window.addEventListener("scroll", throttle(updateParallax, 16))
}

// Counter animations
function initCounterAnimations() {
  const counters = document.querySelectorAll("[data-counter]")

  if (counters.length === 0) return

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
  const target = Number.parseInt(element.getAttribute("data-counter"))
  const duration = Number.parseInt(element.getAttribute("data-duration")) || 2000
  const increment = target / (duration / 16)
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

// Hover effects
function initHoverEffects() {
  // Magnetic effect for buttons
  const magneticElements = document.querySelectorAll("[data-magnetic]")

  magneticElements.forEach((element) => {
    element.addEventListener("mousemove", (e) => {
      const rect = element.getBoundingClientRect()
      const x = e.clientX - rect.left - rect.width / 2
      const y = e.clientY - rect.top - rect.height / 2

      const strength = Number.parseFloat(element.getAttribute("data-magnetic")) || 0.3

      element.style.transform = `translate(${x * strength}px, ${y * strength}px)`
    })

    element.addEventListener("mouseleave", () => {
      element.style.transform = "translate(0, 0)"
    })
  })

  // Tilt effect for cards
  const tiltElements = document.querySelectorAll("[data-tilt]")

  tiltElements.forEach((element) => {
    element.addEventListener("mousemove", (e) => {
      const rect = element.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      const centerX = rect.width / 2
      const centerY = rect.height / 2

      const rotateX = ((y - centerY) / centerY) * -10
      const rotateY = ((x - centerX) / centerX) * 10

      element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
    })

    element.addEventListener("mouseleave", () => {
      element.style.transform = "perspective(1000px) rotateX(0) rotateY(0)"
    })
  })
}

// Smooth scroll to anchor links
function initSmoothScroll() {
  const anchorLinks = document.querySelectorAll('a[href^="#"]')

  anchorLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href")

      if (href === "#") return

      const target = document.querySelector(href)

      if (target) {
        e.preventDefault()

        const offsetTop = target.offsetTop - 80 // Account for fixed header

        window.scrollTo({
          top: offsetTop,
          behavior: "smooth",
        })
      }
    })
  })
}

// Stagger animations for lists
function staggerAnimation(elements, delay = 100) {
  elements.forEach((element, index) => {
    setTimeout(() => {
      element.classList.add("animate-in")
    }, index * delay)
  })
}

// Reveal animation for text
function revealText(element, duration = 1000) {
  const text = element.textContent
  const letters = text.split("")

  element.innerHTML = ""

  letters.forEach((letter, index) => {
    const span = document.createElement("span")
    span.textContent = letter === " " ? "\u00A0" : letter
    span.style.opacity = "0"
    span.style.transform = "translateY(20px)"
    span.style.transition = `all 0.3s ease ${index * 50}ms`
    element.appendChild(span)

    setTimeout(() => {
      span.style.opacity = "1"
      span.style.transform = "translateY(0)"
    }, 100)
  })
}

// Morphing shapes animation
function morphShape(element, shapes, duration = 2000) {
  let currentIndex = 0

  setInterval(() => {
    currentIndex = (currentIndex + 1) % shapes.length
    element.style.clipPath = shapes[currentIndex]
  }, duration)
}

// Particle effect
function createParticles(container, count = 50) {
  for (let i = 0; i < count; i++) {
    const particle = document.createElement("div")
    particle.className = "particle"

    // Random position and animation
    particle.style.left = Math.random() * 100 + "%"
    particle.style.animationDelay = Math.random() * 2 + "s"
    particle.style.animationDuration = Math.random() * 3 + 2 + "s"

    container.appendChild(particle)
  }
}

// Utility function for throttling
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

// CSS for animations
const animationStyles = `
    [data-aos] {
        opacity: 0;
        transition: all 0.6s ease;
    }
    
    [data-aos="fade-up"] {
        transform: translateY(30px);
    }
    
    [data-aos="fade-down"] {
        transform: translateY(-30px);
    }
    
    [data-aos="fade-left"] {
        transform: translateX(30px);
    }
    
    [data-aos="fade-right"] {
        transform: translateX(-30px);
    }
    
    [data-aos="zoom-in"] {
        transform: scale(0.8);
    }
    
    [data-aos="flip-up"] {
        transform: rotateX(90deg);
        transform-origin: center bottom;
    }
    
    .aos-animate {
        opacity: 1;
        transform: none;
    }
    
    .counting {
        transform: scale(1.05);
        transition: transform 0.3s ease;
    }
    
    [data-magnetic] {
        transition: transform 0.3s ease;
    }
    
    [data-tilt] {
        transition: transform 0.3s ease;
    }
    
    .animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        animation: float linear infinite;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
`

// Inject animation styles
const styleSheet = document.createElement("style")
styleSheet.textContent = animationStyles
document.head.appendChild(styleSheet)

// Initialize smooth scroll
document.addEventListener("DOMContentLoaded", initSmoothScroll)
