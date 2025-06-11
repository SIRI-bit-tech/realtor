document.addEventListener('DOMContentLoaded', function() {
  // Avatar fallback
  var avatarImg = document.querySelector('.profile-avatar img');
  if (avatarImg) {
    avatarImg.onerror = function() {
      this.style.display = 'none';
      var placeholder = document.querySelector('.avatar-placeholder');
      if (placeholder) placeholder.style.display = 'flex';
    };
  }

  // Copy to clipboard for email/phone
  function addCopy(selector) {
    var el = document.querySelector(selector);
    if (el) {
      el.style.cursor = 'pointer';
      el.title = 'Click to copy';
      el.addEventListener('click', function() {
        navigator.clipboard.writeText(el.textContent.trim());
        showToast('Copied!');
      });
    }
  }
  addCopy('.profile-email');
  addCopy('.profile-phone');

  // Toast
  function showToast(msg) {
    var toast = document.createElement('div');
    toast.textContent = msg;
    toast.style.position = 'fixed';
    toast.style.bottom = '32px';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%)';
    toast.style.background = '#2979ff';
    toast.style.color = '#fff';
    toast.style.padding = '10px 24px';
    toast.style.borderRadius = '8px';
    toast.style.fontSize = '1em';
    toast.style.zIndex = 9999;
    toast.style.boxShadow = '0 2px 8px rgba(41,121,255,0.12)';
    document.body.appendChild(toast);
    setTimeout(function() {
      toast.remove();
    }, 1200);
  }
}); 