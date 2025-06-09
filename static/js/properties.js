// Properties page JavaScript functionality
document.addEventListener("DOMContentLoaded", () => {
  initPropertyFilters()
  initPropertyMap()
  initPropertyGallery()
  initFavoriteButtons()
  initPropertySearch()
  initViewTracking()
  initPropertyComparison()
})

// Property filtering with HTMX
function initPropertyFilters() {
  const filterForm = document.getElementById("property-filters")
  const priceRange = document.getElementById("price-range")
  const priceMin = document.getElementById("price-min")
  const priceMax = document.getElementById("price-max")

  if (priceRange) {
    // Initialize price range slider
    initPriceRangeSlider(priceRange, priceMin, priceMax)
  }

  // Auto-submit form on filter changes
  if (filterForm) {
    const filterInputs = filterForm.querySelectorAll("select, input[type='checkbox']")

    filterInputs.forEach((input) => {
      input.addEventListener(
        "change",
        debounce(() => {
          htmx.trigger(filterForm, "submit")
        }, 300),
      )
    })
  }

  // Clear filters
  const clearFiltersBtn = document.getElementById("clear-filters")
  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener("click", () => {
      filterForm.reset()
      htmx.trigger(filterForm, "submit")
    })
  }
}

// Price range slider
function initPriceRangeSlider(rangeElement, minInput, maxInput) {
  const minPrice = Number.parseInt(rangeElement.dataset.min) || 0
  const maxPrice = Number.parseInt(rangeElement.dataset.max) || 1000000

  const currentMin = Number.parseInt(minInput.value) || minPrice
  const currentMax = Number.parseInt(maxInput.value) || maxPrice

  // Create dual range slider
  const slider = document.createElement("div")
  slider.className = "price-slider"
  slider.innerHTML = `
    <div class="slider-track"></div>
    <div class="slider-range"></div>
    <input type="range" class="slider-min" min="${minPrice}" max="${maxPrice}" value="${currentMin}" step="1000">
    <input type="range" class="slider-max" min="${minPrice}" max="${maxPrice}" value="${currentMax}" step="1000">
  `

  rangeElement.appendChild(slider)

  const sliderMin = slider.querySelector(".slider-min")
  const sliderMax = slider.querySelector(".slider-max")
  const sliderRange = slider.querySelector(".slider-range")

  function updateSlider() {
    const minVal = Number.parseInt(sliderMin.value)
    const maxVal = Number.parseInt(sliderMax.value)

    if (minVal >= maxVal) {
      sliderMin.value = maxVal - 1000
    }

    const minPercent = ((sliderMin.value - minPrice) / (maxPrice - minPrice)) * 100
    const maxPercent = ((sliderMax.value - minPrice) / (maxPrice - minPrice)) * 100

    sliderRange.style.left = minPercent + "%"
    sliderRange.style.width = maxPercent - minPercent + "%"

    minInput.value = sliderMin.value
    maxInput.value = sliderMax.value

    // Update display
    updatePriceDisplay(sliderMin.value, sliderMax.value)
  }

  function updatePriceDisplay(min, max) {
    const display = rangeElement.querySelector(".price-display")
    if (display) {
      display.textContent = `$${formatPrice(min)} - $${formatPrice(max)}`
    }
  }

  sliderMin.addEventListener("input", updateSlider)
  sliderMax.addEventListener("input", updateSlider)

  updateSlider()
}

// Property map functionality
function initPropertyMap() {
  const mapContainer = document.getElementById("property-map")
  if (!mapContainer) return

  // Initialize map (using Leaflet as example)
  const map = L.map("property-map").setView([40.7128, -74.006], 10)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map)

  // Load property markers
  fetch("/properties/api/map-data/")
    .then((response) => response.json())
    .then((data) => {
      data.markers.forEach((property) => {
        const marker = L.marker([property.lat, property.lng]).addTo(map).bindPopup(createPropertyPopup(property))

        marker.on("click", () => {
          highlightPropertyCard(property.id)
        })
      })
    })
    .catch((error) => console.error("Error loading map data:", error))
}

function createPropertyPopup(property) {
  return `
    <div class="property-popup">
      <h4>${property.title}</h4>
      <p class="price">$${formatPrice(property.price)}</p>
      <p class="features">${property.bedrooms} bed • ${property.bathrooms} bath • ${formatPrice(property.square_feet)} sq ft</p>
      <a href="${property.url}" class="btn btn-sm btn-primary">View Details</a>
    </div>
  `
}

function highlightPropertyCard(propertyId) {
  // Remove existing highlights
  document.querySelectorAll(".property-card.highlighted").forEach((card) => {
    card.classList.remove("highlighted")
  })

  // Highlight the selected property card
  const propertyCard = document.querySelector(`[data-property-id="${propertyId}"]`)
  if (propertyCard) {
    propertyCard.classList.add("highlighted")
    propertyCard.scrollIntoView({ behavior: "smooth", block: "center" })
  }
}

// Property gallery functionality
function initPropertyGallery() {
  const galleries = document.querySelectorAll(".property-gallery")

  galleries.forEach((gallery) => {
    const mainImage = gallery.querySelector(".main-image img")
    const thumbnails = gallery.querySelectorAll(".thumbnail")
    const prevBtn = gallery.querySelector(".gallery-prev")
    const nextBtn = gallery.querySelector(".gallery-next")

    let currentIndex = 0
    const images = Array.from(thumbnails).map((thumb) => ({
      src: thumb.dataset.fullsize,
      alt: thumb.querySelector("img").alt,
    }))

    // Thumbnail clicks
    thumbnails.forEach((thumb, index) => {
      thumb.addEventListener("click", () => {
        currentIndex = index
        updateMainImage()
        updateThumbnails()
      })
    })

    // Navigation buttons
    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        currentIndex = currentIndex > 0 ? currentIndex - 1 : images.length - 1
        updateMainImage()
        updateThumbnails()
      })
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        currentIndex = currentIndex < images.length - 1 ? currentIndex + 1 : 0
        updateMainImage()
        updateThumbnails()
      })
    }

    // Keyboard navigation
    document.addEventListener("keydown", (e) => {
      if (gallery.classList.contains("active")) {
        if (e.key === "ArrowLeft") prevBtn?.click()
        if (e.key === "ArrowRight") nextBtn?.click()
        if (e.key === "Escape") closeGallery()
      }
    })

    function updateMainImage() {
      if (mainImage && images[currentIndex]) {
        mainImage.src = images[currentIndex].src
        mainImage.alt = images[currentIndex].alt
      }
    }

    function updateThumbnails() {
      thumbnails.forEach((thumb, index) => {
        thumb.classList.toggle("active", index === currentIndex)
      })
    }

    // Fullscreen gallery
    mainImage?.addEventListener("click", () => {
      openFullscreenGallery(images, currentIndex)
    })
  })
}

function openFullscreenGallery(images, startIndex) {
  const overlay = document.createElement("div")
  overlay.className = "gallery-overlay"
  overlay.innerHTML = `
    <div class="fullscreen-gallery">
      <button class="gallery-close">&times;</button>
      <button class="gallery-prev">&#8249;</button>
      <button class="gallery-next">&#8250;</button>
      <img src="${images[startIndex].src}" alt="${images[startIndex].alt}" class="fullscreen-image">
      <div class="gallery-counter">${startIndex + 1} / ${images.length}</div>
    </div>
  `

  document.body.appendChild(overlay)
  document.body.style.overflow = "hidden"

  let currentIndex = startIndex

  const closeBtn = overlay.querySelector(".gallery-close")
  const prevBtn = overlay.querySelector(".gallery-prev")
  const nextBtn = overlay.querySelector(".gallery-next")
  const image = overlay.querySelector(".fullscreen-image")
  const counter = overlay.querySelector(".gallery-counter")

  function updateGallery() {
    image.src = images[currentIndex].src
    image.alt = images[currentIndex].alt
    counter.textContent = `${currentIndex + 1} / ${images.length}`
  }

  closeBtn.addEventListener("click", closeGallery)
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closeGallery()
  })

  prevBtn.addEventListener("click", () => {
    currentIndex = currentIndex > 0 ? currentIndex - 1 : images.length - 1
    updateGallery()
  })

  nextBtn.addEventListener("click", () => {
    currentIndex = currentIndex < images.length - 1 ? currentIndex + 1 : 0
    updateGallery()
  })

  function closeGallery() {
    document.body.removeChild(overlay)
    document.body.style.overflow = ""
  }
}

// Favorite buttons functionality
function initFavoriteButtons() {
  document.addEventListener("click", (e) => {
    if (e.target.closest(".favorite-btn")) {
      const btn = e.target.closest(".favorite-btn")
      const icon = btn.querySelector("i")

      // Add loading state
      btn.classList.add("loading")
      icon.className = "icon-spinner"
    }
  })

  // Handle HTMX responses for favorites
  document.body.addEventListener("htmx:afterSwap", (e) => {
    if (e.target.classList.contains("favorite-btn")) {
      const btn = e.target
      const icon = btn.querySelector("i")

      btn.classList.remove("loading")

      // Animate the heart
      if (btn.classList.contains("favorited")) {
        icon.className = "icon-heart-filled"
        btn.classList.add("pulse")
        setTimeout(() => btn.classList.remove("pulse"), 300)
      } else {
        icon.className = "icon-heart"
      }
    }
  })
}

// Property search functionality
function initPropertySearch() {
  const searchInput = document.getElementById("property-search")
  const searchResults = document.getElementById("search-results")

  if (searchInput) {
    searchInput.addEventListener(
      "input",
      debounce((e) => {
        const query = e.target.value.trim()

        if (query.length >= 2) {
          fetch(`/search/suggestions/?q=${encodeURIComponent(query)}`)
            .then((response) => response.text())
            .then((html) => {
              searchResults.innerHTML = html
              searchResults.classList.add("show")
            })
            .catch((error) => {
              console.error("Search error:", error)
              searchResults.classList.remove("show")
            })
        } else {
          searchResults.classList.remove("show")
        }
      }, 300),
    )

    // Hide results when clicking outside
    document.addEventListener("click", (e) => {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.classList.remove("show")
      }
    })
  }
}

// View tracking
function initViewTracking() {
  const propertyId = document.querySelector("[data-property-id]")?.dataset.propertyId

  if (propertyId) {
    // Track view after user has been on page for 3 seconds
    setTimeout(() => {
      fetch(`/properties/track-view/${propertyId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "Content-Type": "application/json",
        },
      }).catch((error) => console.error("View tracking error:", error))
    }, 3000)
  }
}

// Utility functions
function formatPrice(price) {
  return new Intl.NumberFormat("en-US").format(price)
}

function getCsrfToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]")?.value || ""
}

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

// Property comparison functionality
function initPropertyComparison() {
  const compareButtons = document.querySelectorAll(".compare-btn")
  const comparePanel = document.getElementById("compare-panel")
  let comparedProperties = JSON.parse(localStorage.getItem("comparedProperties") || "[]")

  compareButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault()
      const propertyId = btn.dataset.propertyId
      const propertyData = {
        id: propertyId,
        title: btn.dataset.title,
        price: btn.dataset.price,
        image: btn.dataset.image,
        url: btn.dataset.url,
      }

      if (comparedProperties.find((p) => p.id === propertyId)) {
        removeFromComparison(propertyId)
      } else {
        addToComparison(propertyData)
      }

      updateComparePanel()
      updateCompareButtons()
    })
  })

  function addToComparison(property) {
    if (comparedProperties.length >= 3) {
      showNotification("You can compare up to 3 properties", "warning")
      return
    }

    comparedProperties.push(property)
    localStorage.setItem("comparedProperties", JSON.stringify(comparedProperties))
    showNotification("Property added to comparison", "success")
  }

  function removeFromComparison(propertyId) {
    comparedProperties = comparedProperties.filter((p) => p.id !== propertyId)
    localStorage.setItem("comparedProperties", JSON.stringify(comparedProperties))
    showNotification("Property removed from comparison", "info")
  }

  function updateComparePanel() {
    if (!comparePanel) return

    if (comparedProperties.length > 0) {
      comparePanel.classList.add("show")
      comparePanel.innerHTML = `
        <div class="compare-header">
          <h4>Compare Properties (${comparedProperties.length}/3)</h4>
          <button class="btn btn-sm btn-primary" onclick="window.open('/properties/compare/?ids=${comparedProperties.map((p) => p.id).join(",")}', '_blank')">
            Compare Now
          </button>
          <button class="compare-clear" onclick="clearComparison()">Clear All</button>
        </div>
        <div class="compare-items">
          ${comparedProperties
            .map(
              (property) => `
            <div class="compare-item">
              <img src="${property.image}" alt="${property.title}">
              <h5>${property.title}</h5>
              <p>$${formatPrice(property.price)}</p>
              <button class="remove-compare" onclick="removeFromComparison('${property.id}')">×</button>
            </div>
          `,
            )
            .join("")}
        </div>
      `
    } else {
      comparePanel.classList.remove("show")
    }
  }

  function updateCompareButtons() {
    compareButtons.forEach((btn) => {
      const propertyId = btn.dataset.propertyId
      const isCompared = comparedProperties.find((p) => p.id === propertyId)

      btn.classList.toggle("active", !!isCompared)
      btn.textContent = isCompared ? "Remove from Compare" : "Compare"
    })
  }

  // Initialize on page load
  updateComparePanel()
  updateCompareButtons()

  // Global functions for inline handlers
  window.clearComparison = () => {
    comparedProperties = []
    localStorage.removeItem("comparedProperties")
    updateComparePanel()
    updateCompareButtons()
    showNotification("Comparison cleared", "info")
  }

  window.removeFromComparison = removeFromComparison
}

// Initialize comparison on page load
document.addEventListener("DOMContentLoaded", initPropertyComparison)
