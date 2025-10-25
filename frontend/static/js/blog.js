
// Share Functionality (global functions)
window.shareOnX = function() {
  try {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(document.title);
    window.open(`https://x.com/intent/tweet?url=${url}&text=${text}`, '_blank', 'width=600,height=400');
  } catch (error) {
    console.warn('X share failed:', error);
  }
}

window.shareOnFacebook = function() {
  try {
    const url = encodeURIComponent(window.location.href);
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank', 'width=600,height=400');
  } catch (error) {
    console.warn('Facebook share failed:', error);
  }
}

window.shareOnLinkedIn = function() {
  try {
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.title);
    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}&title=${title}`, '_blank', 'width=600,height=400');
  } catch (error) {
    console.warn('LinkedIn share failed:', error);
  }
}

window.copyLink = function() {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(window.location.href).then(function() {
        showCopySuccess();
      }).catch(function() {
        fallbackCopyTextToClipboard();
      });
    } else {
      fallbackCopyTextToClipboard();
    }
  } catch (error) {
    console.warn('Copy link failed:', error);
    fallbackCopyTextToClipboard();
  }
}

function fallbackCopyTextToClipboard() {
  try {
    const textArea = document.createElement('textarea');
    textArea.value = window.location.href;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    showCopySuccess();
  } catch (error) {
    console.warn('Fallback copy failed:', error);
  }
}

function showCopySuccess() {
  const btn = document.querySelector('.share-btn.copy');
  if (btn) {
    const originalText = btn.innerHTML;
    btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>Copied!';
    setTimeout(() => {
      btn.innerHTML = originalText;
    }, 2000);
  }
}

// Reading Progress Indicator
function initReadingProgress() {
  document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('navbar');
    const navbarheight = navbar.offsetHeight;
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
      position: fixed;
      top: ${navbarheight}px;
      left: 0;
      width: 0%;
      height: 3px;
      background: linear-gradient(90deg, var(--color-primary-500), var(--color-primary-600));
      z-index: 9999;
      transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', function () {
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;
      progressBar.style.width = scrolled + '%';
    });
  });
}

// Initialize all blog functionality
initReadingProgress();
