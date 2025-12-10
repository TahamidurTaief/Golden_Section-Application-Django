// Service Request Form Enhancement Script
document.addEventListener('DOMContentLoaded', function() {
    // Initialize datetime input minimum date
    const dateTimeInput = document.querySelector('input[type="datetime-local"]');
    if (dateTimeInput) {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        dateTimeInput.setAttribute('min', minDateTime);
    }

    // Enhanced file validation
    function validateFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'video/mp4', 'video/quicktime'];
        const maxSize = 10 * 1024 * 1024; // 10MB
        
        if (!validTypes.includes(file.type)) {
            showNotification('Invalid file type. Only JPG, PNG, and MP4 files are allowed.', 'error');
            return false;
        }
        
        if (file.size > maxSize) {
            showNotification('File size too large. Maximum size is 10MB.', 'error');
            return false;
        }
        
        return true;
    }

    // Notification system
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 350px;';
        
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Form validation enhancement
    function validateStep(stepIndex, formData) {
        const validations = {
            0: () => { // Basic Information
                const errors = [];
                if (!formData.firstName?.trim()) errors.push('First name is required');
                if (!formData.lastName?.trim()) errors.push('Last name is required');
                if (!formData.email?.trim()) errors.push('Email is required');
                if (!formData.phone?.trim()) errors.push('Phone number is required');
                if (!formData.bookingEstimate) errors.push('Booking estimate is required');
                
                // Email validation
                if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
                    errors.push('Please enter a valid email address');
                }
                
                // Phone validation (basic)
                if (formData.phone && !/^[\+]?[0-9\s\-\(\)]{10,}$/.test(formData.phone)) {
                    errors.push('Please enter a valid phone number');
                }
                
                return errors;
            },
            1: () => { // Booking Schedule
                const errors = [];
                if (!formData.bookingDateTime) errors.push('Booking date and time is required');
                if (!formData.hourlyRate) errors.push('Please select hourly rate');
                
                // Date validation
                if (formData.bookingDateTime) {
                    const selectedDate = new Date(formData.bookingDateTime);
                    const now = new Date();
                    if (selectedDate <= now) {
                        errors.push('Booking date must be in the future');
                    }
                }
                
                return errors;
            },
            2: () => { // Collection Address
                const errors = [];
                if (!formData.collectionAddress?.trim()) errors.push('Collection address is required');
                if (!formData.collectionPostalCode?.trim()) errors.push('Postal code is required');
                if (!formData.collectionCity?.trim()) errors.push('City is required');
                if (!formData.collectionPropertyType) errors.push('Property type is required');
                if (!formData.collectionFloorLevel) errors.push('Floor level is required');
                return errors;
            },
            3: () => { // Delivery Address
                const errors = [];
                if (!formData.deliveryAddress?.trim()) errors.push('Delivery address is required');
                if (!formData.deliveryPostalCode?.trim()) errors.push('Postal code is required');
                if (!formData.deliveryCity?.trim()) errors.push('City is required');
                if (!formData.deliveryPropertyType) errors.push('Property type is required');
                if (!formData.deliveryFloorLevel) errors.push('Floor level is required');
                return errors;
            }
        };
        
        return validations[stepIndex] ? validations[stepIndex]() : [];
    }

    // Smooth scrolling for step changes
    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    // Auto-save form data to localStorage
    function saveFormData(formData) {
        try {
            localStorage.setItem('serviceRequestFormData', JSON.stringify(formData));
        } catch (e) {
            console.warn('Could not save form data to localStorage:', e);
        }
    }

    // Load form data from localStorage
    function loadFormData() {
        try {
            const saved = localStorage.getItem('serviceRequestFormData');
            return saved ? JSON.parse(saved) : null;
        } catch (e) {
            console.warn('Could not load form data from localStorage:', e);
            return null;
        }
    }

    // Clear saved form data
    function clearSavedData() {
        try {
            localStorage.removeItem('serviceRequestFormData');
        } catch (e) {
            console.warn('Could not clear saved form data:', e);
        }
    }

    // Accessibility improvements
    function updateStepAccessibility(currentStep) {
        const steps = document.querySelectorAll('.wizard-progress li');
        steps.forEach((step, index) => {
            if (index < currentStep) {
                step.setAttribute('aria-label', `Step ${index + 1}: Completed`);
            } else if (index === currentStep) {
                step.setAttribute('aria-label', `Step ${index + 1}: Current step`);
            } else {
                step.setAttribute('aria-label', `Step ${index + 1}: Not completed`);
            }
        });
    }

    // Keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // Allow Escape key to close modals or go back
        if (e.key === 'Escape') {
            const activeElement = document.activeElement;
            if (activeElement && activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
                // Could implement step navigation here
            }
        }
    });

    // Responsive image loading
    function optimizeImages() {
        const images = document.querySelectorAll('img[loading="lazy"]');
        
        // Intersection Observer for lazy loading
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    // Initialize enhancements
    optimizeImages();

    // Expose utility functions globally for Alpine.js
    window.ServiceRequestUtils = {
        showNotification,
        validateStep,
        scrollToTop,
        saveFormData,
        loadFormData,
        clearSavedData,
        validateFile
    };

    console.log('Service Request Form enhancements loaded successfully!');
});

// Custom Alpine.js directives
document.addEventListener('alpine:init', () => {
    Alpine.directive('validate', (el, { expression }, { evaluate }) => {
        el.addEventListener('input', () => {
            const value = el.value;
            const validation = evaluate(expression);
            
            // Add validation styling
            if (validation && !validation(value)) {
                el.classList.add('is-invalid');
            } else {
                el.classList.remove('is-invalid');
            }
        });
    });
    
    Alpine.directive('auto-save', (el, { expression }, { evaluate, evaluateLater }) => {
        const saveData = evaluateLater(expression);
        
        el.addEventListener('input', Alpine.debounce(() => {
            saveData();
        }, 1000));
    });
});