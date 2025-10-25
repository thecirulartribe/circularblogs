// Thank You Page Enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add confetti effect for community applications
    const urlParams = new URLSearchParams(window.location.search);
    const isCommunityThankYou = urlParams.get('community');

    if (isCommunityThankYou) {
        // Create confetti effect
        createConfetti();

        // Add email reminder after 5 seconds
        setTimeout(showEmailReminder, 5000);

        // Add contact link tracking
        trackContactClicks();
    }

    // Add smooth scroll animations
    addScrollAnimations();

});

function createConfetti() {
    const colors = ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
            createConfettiPiece(colors[Math.floor(Math.random() * colors.length)]);
        }, i * 50);
    }
}

function createConfettiPiece(color) {
    const confetti = document.createElement('div');
    confetti.style.cssText = `
        position: fixed;
        width: 10px;
        height: 10px;
        background: ${color};
        top: -10px;
        left: ${Math.random() * 100}vw;
        z-index: 1000;
        pointer-events: none;
        border-radius: 50%;
        animation: confettiFall ${2 + Math.random() * 3}s linear forwards;
    `;

    document.body.appendChild(confetti);

    // Remove confetti after animation
    setTimeout(() => {
        confetti.remove();
    }, 5000);
}

function showEmailReminder() {
    const reminder = document.createElement('div');
    reminder.className = 'email-reminder';
    reminder.innerHTML = `
        <div class="reminder-content">
            <div class="reminder-icon">📧</div>
            <div class="reminder-text">
                <strong>Don't forget!</strong> Check your email for next steps.
            </div>
            <button class="reminder-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;

    reminder.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        z-index: 1000;
        max-width: 300px;
        animation: slideInRight 0.5s ease-out;
    `;

    document.body.appendChild(reminder);

    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (reminder.parentNode) {
            reminder.style.animation = 'slideOutRight 0.5s ease-out forwards';
            setTimeout(() => reminder.remove(), 500);
        }
    }, 10000);
}

function trackContactClicks() {
    const contactLinks = document.querySelectorAll('.contact-link');
    contactLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Track contact link clicks
            console.log('Contact link clicked');

            // Show success message
            showToast('Opening email client... We\'ll respond within 24 hours! 📧');
        });
    });
}

function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll('.step-item, .link-card, .stat-item');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: #22c55e;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        font-weight: 500;
        animation: toastSlideUp 0.3s ease-out;
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'toastSlideDown 0.3s ease-out forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes confettiFall {
        to {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }

    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    @keyframes toastSlideUp {
        from {
            transform: translateX(-50%) translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }
    }

    @keyframes toastSlideDown {
        from {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }
        to {
            transform: translateX(-50%) translateY(100%);
            opacity: 0;
        }
    }

    .reminder-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .reminder-icon {
        font-size: 24px;
        flex-shrink: 0;
    }

    .reminder-text {
        flex: 1;
        font-size: 14px;
        line-height: 1.4;
    }

    .reminder-close {
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
        color: #666;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background 0.3s ease;
    }

    .reminder-close:hover {
        background: rgba(0,0,0,0.1);
    }

    .status-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .status-icon {
        font-size: 24px;
        flex-shrink: 0;
    }

    .status-text {
        flex: 1;
        font-size: 14px;
        line-height: 1.4;
        color: var(--color-primary-700);
    }
`;
document.head.appendChild(style);
