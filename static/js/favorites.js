document.addEventListener('DOMContentLoaded', function() {
  // Remove favorite
  document.querySelectorAll('.remove-favorite-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const favId = btn.dataset.favoriteId;
      const propertyId = btn.dataset.propertyId;
      fetch(`/properties/favorite/${propertyId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCSRFToken(),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: new URLSearchParams({ action: 'remove' })
      })
      .then(res => {
        if (!res.ok) throw new Error('Failed to remove favorite');
        // Remove card from UI
        btn.closest('.favorite-card').remove();
        showToast('Removed from favorites');
      })
      .catch(() => showToast('Error removing favorite', true));
    });
  });

  // Toast
  function showToast(msg, error) {
    let toast = document.createElement('div');
    toast.textContent = msg;
    toast.style.position = 'fixed';
    toast.style.bottom = '32px';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%)';
    toast.style.background = error ? '#b94a48' : 'var(--accent-color)';
    toast.style.color = '#fff';
    toast.style.padding = '10px 24px';
    toast.style.borderRadius = '8px';
    toast.style.fontSize = '1em';
    toast.style.zIndex = 9999;
    toast.style.boxShadow = '0 2px 8px rgba(212,175,55,0.12)';
    document.body.appendChild(toast);
    setTimeout(function() {
      toast.remove();
    }, 1400);
  }

  // CSRF helper
  function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === 'csrftoken=') {
          cookieValue = decodeURIComponent(cookie.substring(10));
          break;
        }
      }
    }
    return cookieValue;
  }
}); 