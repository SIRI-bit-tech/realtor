import { Chart } from "@/components/ui/chart"
// Analytics Dashboard JavaScript
document.addEventListener("DOMContentLoaded", () => {
  initAnalyticsDashboard()
})

function initAnalyticsDashboard() {
  // Initialize date range picker if available
  const dateRangePicker = document.querySelector(".date-range-picker")
  if (dateRangePicker) {
    // Initialize date range picker functionality
    // This would typically use a library like flatpickr or daterangepicker
  }

  // Initialize export functionality
  const exportButtons = document.querySelectorAll("[data-export]")
  exportButtons.forEach((button) => {
    button.addEventListener("click", handleExport)
  })

  // Initialize any tooltips
  initTooltips()

  // Initialize table sorting if needed
  initTableSorting()

  // Initialize real-time updates
  initRealTimeUpdates()
}

function handleExport(e) {
  const type = e.currentTarget.dataset.export
  const days = e.currentTarget.dataset.days || 30

  // Show loading indicator
  showNotification("Preparing export...", "info")

  // Fetch export data
  fetch(`/analytics/export/?type=${type}&days=${days}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Export failed")
      }
      return response.json()
    })
    .then((data) => {
      // Convert data to CSV
      const csv = convertToCSV(data.data)

      // Create download link
      downloadCSV(csv, `${type}_${days}_days.csv`)

      showNotification("Export complete!", "success")
    })
    .catch((error) => {
      console.error("Export error:", error)
      showNotification("Export failed. Please try again.", "error")
    })
}

function convertToCSV(data) {
  if (!data || data.length === 0) {
    return ""
  }

  // Get headers from first object
  const headers = Object.keys(data[0])

  // Create CSV content
  const csvContent = [
    headers.join(","),
    ...data.map((row) =>
      headers
        .map((header) => {
          const value = row[header]
          // Escape commas and quotes
          if (typeof value === "string" && (value.includes(",") || value.includes('"'))) {
            return `"${value.replace(/"/g, '""')}"`
          }
          return value
        })
        .join(","),
    ),
  ].join("\n")

  return csvContent
}

function downloadCSV(csv, filename) {
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" })
  const link = document.createElement("a")

  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob)
    link.setAttribute("href", url)
    link.setAttribute("download", filename)
    link.style.visibility = "hidden"
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

function initTooltips() {
  // Initialize tooltips for chart elements
  const tooltipElements = document.querySelectorAll("[data-tooltip]")
  tooltipElements.forEach((element) => {
    element.addEventListener("mouseenter", showTooltip)
    element.addEventListener("mouseleave", hideTooltip)
  })
}

function showTooltip(e) {
  const text = e.currentTarget.dataset.tooltip
  const tooltip = document.createElement("div")
  tooltip.className = "tooltip"
  tooltip.textContent = text

  document.body.appendChild(tooltip)

  // Position tooltip
  const rect = e.currentTarget.getBoundingClientRect()
  tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + "px"
  tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + "px"
}

function hideTooltip() {
  const tooltip = document.querySelector(".tooltip")
  if (tooltip) {
    tooltip.remove()
  }
}

function initTableSorting() {
  const tables = document.querySelectorAll(".data-table")
  tables.forEach((table) => {
    const headers = table.querySelectorAll("th")
    headers.forEach((header, index) => {
      header.style.cursor = "pointer"
      header.addEventListener("click", () => sortTable(table, index))
    })
  })
}

function sortTable(table, columnIndex) {
  const tbody = table.querySelector("tbody")
  const rows = Array.from(tbody.querySelectorAll("tr"))

  // Determine sort direction
  const currentSort = table.dataset.sortColumn
  const currentDirection = table.dataset.sortDirection || "asc"
  const newDirection = currentSort == columnIndex && currentDirection === "asc" ? "desc" : "asc"

  // Sort rows
  rows.sort((a, b) => {
    const aValue = a.cells[columnIndex].textContent.trim()
    const bValue = b.cells[columnIndex].textContent.trim()

    // Try to parse as numbers
    const aNum = Number.parseFloat(aValue.replace(/[^0-9.-]/g, ""))
    const bNum = Number.parseFloat(bValue.replace(/[^0-9.-]/g, ""))

    let comparison = 0
    if (!isNaN(aNum) && !isNaN(bNum)) {
      comparison = aNum - bNum
    } else {
      comparison = aValue.localeCompare(bValue)
    }

    return newDirection === "asc" ? comparison : -comparison
  })

  // Update table
  rows.forEach((row) => tbody.appendChild(row))

  // Update sort indicators
  table.dataset.sortColumn = columnIndex
  table.dataset.sortDirection = newDirection

  // Update header indicators
  const headers = table.querySelectorAll("th")
  headers.forEach((header, index) => {
    header.classList.remove("sort-asc", "sort-desc")
    if (index === columnIndex) {
      header.classList.add(`sort-${newDirection}`)
    }
  })
}

function showNotification(message, type = "info") {
  const notification = document.createElement("div")
  notification.className = `notification notification-${type}`
  notification.textContent = message

  // Add notification styles
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 4px;
    color: white;
    font-weight: 500;
    z-index: 1000;
    animation: slideIn 0.3s ease-out;
  `

  // Set background color based on type
  switch (type) {
    case "success":
      notification.style.backgroundColor = "#10b981"
      break
    case "error":
      notification.style.backgroundColor = "#ef4444"
      break
    case "info":
    default:
      notification.style.backgroundColor = "#3b82f6"
      break
  }

  document.body.appendChild(notification)

  // Auto-remove after 3 seconds
  setTimeout(() => {
    notification.remove()
  }, 3000)
}

// Real-time updates functionality
function initRealTimeUpdates() {
  // Update statistics every 30 seconds
  setInterval(updateStatistics, 30000)

  // Update charts every 60 seconds
  setInterval(updateCharts, 60000)
}

function updateStatistics() {
  const days = new URLSearchParams(window.location.search).get("days") || 30

  fetch(`/analytics/api/stats/?days=${days}`)
    .then((response) => response.json())
    .then((data) => {
      // Update stat cards
      updateStatCard("total_page_views", data.total_page_views)
      updateStatCard("total_property_views", data.total_property_views)
      updateStatCard("total_searches", data.total_searches)
    })
    .catch((error) => {
      console.error("Error updating statistics:", error)
    })
}

function updateStatCard(statName, newValue) {
  const statElement = document.querySelector(`[data-stat="${statName}"]`)
  if (statElement) {
    const currentValue = Number.parseInt(statElement.textContent)
    if (currentValue !== newValue) {
      // Animate the change
      animateNumber(statElement, currentValue, newValue)
    }
  }
}

function animateNumber(element, start, end) {
  const duration = 1000 // 1 second
  const startTime = performance.now()

  function update(currentTime) {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)

    const current = Math.floor(start + (end - start) * progress)
    element.textContent = current.toLocaleString()

    if (progress < 1) {
      requestAnimationFrame(update)
    }
  }

  requestAnimationFrame(update)
}

function updateCharts() {
  const days = new URLSearchParams(window.location.search).get("days") || 30

  fetch(`/analytics/api/chart-data/?days=${days}`)
    .then((response) => response.json())
    .then((data) => {
      // Update page views chart if it exists
      if (window.pageViewsChart) {
        window.pageViewsChart.data.labels = data.daily_views.map((item) => new Date(item.day).toLocaleDateString())
        window.pageViewsChart.data.datasets[0].data = data.daily_views.map((item) => item.count)
        window.pageViewsChart.update()
      }
    })
    .catch((error) => {
      console.error("Error updating charts:", error)
    })
}

// Chart.js default configuration
if (typeof Chart !== "undefined") {
  Chart.defaults.font.family = "'Inter', sans-serif"
  Chart.defaults.color = "#6b7280"
  Chart.defaults.plugins.legend.display = true
  Chart.defaults.plugins.legend.position = "bottom"
  Chart.defaults.responsive = true
  Chart.defaults.maintainAspectRatio = false
}
