// Write for Us Community Application Form Enhancement
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('communityApplicationForm');
    const submitButton = form?.querySelector('.form-submit');
    const inputs = form?.querySelectorAll('.form-input');

    if (!form) return;

    // Add loading state to submit button
    form.addEventListener('submit', function (e) {
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="loading-spinner"></span> Joining Community...';
            submitButton.style.opacity = '0.7';
        }
    });

    // Add real-time validation feedback
    inputs?.forEach(input => {
        input.addEventListener('blur', function () {
            validateField(this);
        });

        input.addEventListener('input', function () {
            // Clear error state when user starts typing
            this.classList.remove('error');
            const errorElement = this.parentNode.querySelector('.field-error');
            if (errorElement) {
                errorElement.style.opacity = '0';
                setTimeout(() => errorElement.remove(), 300);
            }
        });
    });

    // Field validation function
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Name validation
        if (field.name === 'name') {
            if (value.length < 2) {
                isValid = false;
                errorMessage = 'Name must be at least 2 characters long.';
            }
        }

        // Email validation
        if (field.name === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address.';
            }
        }

        // Message validation
        if (field.name === 'message') {
            if (value.length < 50) {
                isValid = false;
                errorMessage = 'Please provide more details about yourself (at least 50 characters).';
            }
        }

        // Update field appearance
        if (!isValid) {
            field.classList.add('error');
            showFieldError(field, errorMessage);
        } else {
            field.classList.remove('error');
            clearFieldError(field);
        }

        return isValid;
    }

    // Show field error
    function showFieldError(field, message) {
        clearFieldError(field);
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.textContent = message;
        errorElement.style.opacity = '0';
        field.parentNode.appendChild(errorElement);

        // Fade in error
        setTimeout(() => {
            errorElement.style.opacity = '1';
        }, 10);
    }

    // Clear field error
    function clearFieldError(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.style.opacity = '0';
            setTimeout(() => existingError.remove(), 300);
        }
    }

    // Character counter for message field
    const messageField = form.querySelector('textarea[name="message"]');
    if (messageField) {
        const counter = document.createElement('div');
        counter.className = 'character-counter';
        counter.style.cssText = `
            font-size: 0.875rem;
            color: var(--color-text-secondary);
            text-align: right;
            margin-top: 0.25rem;
            transition: color 0.3s ease;
        `;
        messageField.parentNode.appendChild(counter);

        function updateCounter() {
            const length = messageField.value.length;
            counter.textContent = `${length}/50 characters minimum`;

            if (length < 50) {
                counter.style.color = 'var(--color-red-500)';
            } else {
                counter.style.color = 'var(--color-green-500)';
            }
        }

        messageField.addEventListener('input', updateCounter);
        updateCounter(); // Initial count
    }

    // Add smooth animations to form elements
    const formGroups = form.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        group.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

        setTimeout(() => {
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Add loading spinner CSS
const style = document.createElement('style');
style.textContent = `
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
        margin-right: 8px;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .character-counter {
        transition: all 0.3s ease;
    }

    .form-input.error {
        animation: shake 0.5s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);
