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

  document.body.appendChild(notification)

  // Auto-remove after 3 seconds
  setTimeout(() => {
    notification.remove()
  }, 3000)
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
