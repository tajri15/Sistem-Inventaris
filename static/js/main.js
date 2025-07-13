// Main JavaScript file for PT Telkom Indonesia Inventory System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-focus first input in modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = modal.querySelector('input:not([type="hidden"]), select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });

    // Confirm before leaving page with unsaved changes
    let formChanged = false;
    const formInputs = document.querySelectorAll('input, select, textarea');
    formInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            formChanged = true;
        });
    });

    window.addEventListener('beforeunload', function(event) {
        if (formChanged) {
            event.preventDefault();
            event.returnValue = '';
        }
    });

    // Reset form changed flag on form submit
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            formChanged = false;
        });
    });

    // Table row click handler for better UX
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function(event) {
            // Don't trigger if clicking on buttons or links
            if (event.target.closest('button') || event.target.closest('a')) {
                return;
            }
            
            // Add visual feedback
            row.classList.add('table-active');
            setTimeout(function() {
                row.classList.remove('table-active');
            }, 200);
        });
    });

    // Search input enhancement
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    searchInputs.forEach(function(input) {
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                // Add search functionality if needed
                console.log('Search:', input.value);
            }, 300);
        });
    });

    // Number input validation
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = parseFloat(input.value);
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);
            
            if (input.min && value < min) {
                input.setCustomValidity(`Value must be at least ${min}`);
            } else if (input.max && value > max) {
                input.setCustomValidity(`Value must not exceed ${max}`);
            } else {
                input.setCustomValidity('');
            }
        });
    });

    // Add loading state to buttons on form submit
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...';
            }
        });
    });

    // Enhance delete confirmation
    window.confirmDelete = function(id, name, type = 'item') {
        return confirm(`Are you sure you want to delete this ${type}?\n\nName: ${name}\n\nThis action cannot be undone.`);
    };

    // Format currency inputs
    const currencyInputs = document.querySelectorAll('input[name="unit_price"]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            const value = parseFloat(input.value);
            if (!isNaN(value)) {
                input.value = value.toFixed(2);
            }
        });
    });

    // Auto-generate item code suggestion
    const itemNameInput = document.querySelector('input[name="name"]');
    const itemCodeInput = document.querySelector('input[name="code"]');
    
    if (itemNameInput && itemCodeInput) {
        itemNameInput.addEventListener('input', function() {
            if (!itemCodeInput.value) {
                const suggestion = itemNameInput.value
                    .toUpperCase()
                    .replace(/[^A-Z0-9]/g, '')
                    .substring(0, 10);
                
                if (suggestion.length >= 3) {
                    itemCodeInput.placeholder = `Suggestion: ${suggestion}`;
                }
            }
        });
    }

    // Print functionality
    window.printPage = function() {
        window.print();
    };

    // Export functionality placeholder
    window.exportData = function(format) {
        alert(`Export to ${format} functionality would be implemented here.`);
    };

    // Keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl+N for new item/category/warehouse
        if (event.ctrlKey && event.key === 'n') {
            event.preventDefault();
            const addButton = document.querySelector('button[data-bs-target*="Modal"]');
            if (addButton) {
                addButton.click();
            }
        }
        
        // Escape to close modals
        if (event.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });

    // Real-time stock status updates
    function updateStockStatus() {
        const quantityInputs = document.querySelectorAll('input[name="quantity"]');
        const minStockInputs = document.querySelectorAll('input[name="min_stock"]');
        
        function checkStock() {
            const quantity = parseInt(quantityInputs[0]?.value || 0);
            const minStock = parseInt(minStockInputs[0]?.value || 0);
            
            const statusIndicator = document.querySelector('#stock-status');
            if (statusIndicator) {
                if (quantity === 0) {
                    statusIndicator.textContent = 'Out of Stock';
                    statusIndicator.className = 'badge bg-danger';
                } else if (quantity <= minStock) {
                    statusIndicator.textContent = 'Low Stock';
                    statusIndicator.className = 'badge bg-warning';
                } else {
                    statusIndicator.textContent = 'In Stock';
                    statusIndicator.className = 'badge bg-success';
                }
            }
        }
        
        quantityInputs.forEach(input => input.addEventListener('input', checkStock));
        minStockInputs.forEach(input => input.addEventListener('input', checkStock));
    }
    
    updateStockStatus();

    console.log('PT Telkom Indonesia Inventory System initialized successfully!');
});

// Utility functions
const TelkomInventory = {
    // Format currency for display
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR'
        }).format(amount);
    },

    // Format date for display
    formatDate: function(date) {
        return new Intl.DateTimeFormat('id-ID', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },

    // Show notification
    showNotification: function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }, 5000);
        }
    },

    // Validate form data
    validateForm: function(formData) {
        const errors = [];
        
        // Add custom validation logic here
        if (formData.quantity < 0) {
            errors.push('Quantity cannot be negative');
        }
        
        if (formData.unit_price <= 0) {
            errors.push('Unit price must be greater than zero');
        }
        
        return errors;
    }
};

// Make utility functions globally available
window.TelkomInventory = TelkomInventory;
