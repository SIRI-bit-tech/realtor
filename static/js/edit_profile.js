document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('edit-profile-form');
  if (!form) return;
  let submitting = false;

  form.addEventListener('submit', function(e) {
    if (submitting) {
      e.preventDefault();
      return false;
    }
    // Basic validation
    let valid = true;
    form.querySelectorAll('input[required], textarea[required], select[required]').forEach(function(input) {
      if (!input.value.trim()) {
        input.style.borderColor = '#e74c3c';
        valid = false;
      } else {
        input.style.borderColor = '#2979ff';
      }
    });
    if (!valid) {
      e.preventDefault();
      alert('Please fill in all required fields.');
      return false;
    }
    submitting = true;
    // Show loading indicator
    let btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Saving...';
      btn.style.background = '#b0c4de';
    }
  });
}); 