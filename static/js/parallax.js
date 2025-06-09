// Parallax scrolling effects
document.addEventListener("DOMContentLoaded", () => {
  initParallaxEffects()
})

function initParallaxEffects() {
  const parallaxElements = document.querySelectorAll(".hero-background, .cta-background")

  if (parallaxElements.length === 0) return

  // Check if user prefers reduced motion
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches

  if (prefersReducedMotion) return

  window.addEventListener("scroll", throttle(updateParallax, 16))

  function updateParallax() {
    const scrolled = window.pageYOffset
    const rate = scrolled * -0.5

    parallaxElements.forEach((element) => {
      const rect = element.getBoundingClientRect()
      const isVisible = rect.bottom >= 0 && rect.top <= window.innerHeight

      if (isVisible) {
        element.style.transform = `translateY(${rate}px)`
      }
    })
  }
}

// Multi-layer parallax for hero section
function initHeroParallax() {
  const heroSection = document.querySelector(".hero-section")
  const heroContent = document.querySelector(".hero-content")
  const heroBackground = document.querySelector(".hero-background")

  if (!heroSection) return

  window.addEventListener(
    "scroll",
    throttle(() => {
      const scrolled = window.pageYOffset
      const heroHeight = heroSection.offsetHeight
      const scrollProgress = scrolled / heroHeight

      if (scrollProgress <= 1) {
        // Background moves slower (parallax effect)
        if (heroBackground) {
          heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`
        }

        // Content moves at normal speed but with opacity fade
        if (heroContent) {
          const opacity = Math.max(0, 1 - scrollProgress * 1.5)
          heroContent.style.opacity = opacity
          heroContent.style.transform = `translateY(${scrolled * 0.1}px)`
        }
      }
    }, 16),
  )
}

// Initialize hero parallax
document.addEventListener("DOMContentLoaded", initHeroParallax)

// Throttle function (if not already defined in main.js)
if (typeof throttle === "undefined") {
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
}
