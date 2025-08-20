// Survey Form Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeFormInteractivity();
    initializeExpenseCalculations();
    initializeFormValidation();
});

function initializeFormInteractivity() {
    // Handle checkbox changes to enable/disable amount fields
    const expenseCategories = [
        'utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare'
    ];
    
    expenseCategories.forEach(category => {
        const checkbox = document.getElementById(`${category}_check`);
        const amountField = document.getElementById(`${category}_amount`);
        
        if (checkbox && amountField) {
            // Initial state
            updateAmountFieldState(checkbox, amountField);
            
            // Listen for changes
            checkbox.addEventListener('change', function() {
                updateAmountFieldState(checkbox, amountField);
                calculateTotalExpenses();
            });
            
            // Clear amount when disabled
            amountField.addEventListener('input', function() {
                if (!checkbox.checked) {
                    amountField.value = '';
                }
                calculateTotalExpenses();
            });
        }
    });
}

function updateAmountFieldState(checkbox, amountField) {
    if (checkbox.checked) {
        amountField.disabled = false;
        amountField.focus();
        amountField.parentElement.classList.add('expense-enabled');
    } else {
        amountField.disabled = true;
        amountField.value = '';
        amountField.parentElement.classList.remove('expense-enabled');
    }
}

function initializeExpenseCalculations() {
    const incomeField = document.getElementById('total_income');
    const expenseFields = document.querySelectorAll('.expense-amount');
    
    // Add event listeners for real-time calculation
    if (incomeField) {
        incomeField.addEventListener('input', calculateTotalExpenses);
    }
    
    expenseFields.forEach(field => {
        field.addEventListener('input', calculateTotalExpenses);
    });
}

function calculateTotalExpenses() {
    const incomeField = document.getElementById('total_income');
    const summaryCard = document.getElementById('summaryCard');
    
    if (!incomeField || !summaryCard) return;
    
    const income = parseFloat(incomeField.value) || 0;
    let totalExpenses = 0;
    
    // Calculate total expenses from enabled fields
    const expenseCategories = [
        'utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare'
    ];
    
    expenseCategories.forEach(category => {
        const checkbox = document.getElementById(`${category}_check`);
        const amountField = document.getElementById(`${category}_amount`);
        
        if (checkbox && amountField && checkbox.checked && !amountField.disabled) {
            const amount = parseFloat(amountField.value) || 0;
            totalExpenses += amount;
        }
    });
    
    // Update summary display
    updateSummaryDisplay(income, totalExpenses, summaryCard);
}

function updateSummaryDisplay(income, totalExpenses, summaryCard) {
    const summaryIncome = document.getElementById('summaryIncome');
    const summaryExpensesEl = document.getElementById('summaryExpenses');
    const summaryBalance = document.getElementById('summaryBalance');
    const summaryRatio = document.getElementById('summaryRatio');
    
    if (income > 0 || totalExpenses > 0) {
        const balance = income - totalExpenses;
        const ratio = income > 0 ? ((totalExpenses / income) * 100) : 0;
        
        // Update values
        if (summaryIncome) summaryIncome.textContent = formatCurrency(income);
        if (summaryExpensesEl) summaryExpensesEl.textContent = formatCurrency(totalExpenses);
        if (summaryBalance) {
            summaryBalance.textContent = formatCurrency(balance);
            summaryBalance.className = balance >= 0 ? 'text-success' : 'text-danger';
        }
        if (summaryRatio) {
            summaryRatio.textContent = `${ratio.toFixed(1)}%`;
            summaryRatio.className = ratio > 100 ? 'text-danger fw-bold' : ratio > 80 ? 'text-warning fw-bold' : 'text-success';
        }
        
        // Show summary card with animation
        summaryCard.style.display = 'block';
        summaryCard.classList.add('fade-in');
    } else {
        summaryCard.style.display = 'none';
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

function initializeFormValidation() {
    const form = document.getElementById('surveyForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                showValidationErrors();
            }
        });
        
        // Real-time validation for individual fields
        const requiredFields = ['age', 'gender', 'total_income'];
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('blur', function() {
                    validateField(field);
                });
            }
        });
    }
}

function validateForm() {
    let isValid = true;
    const errors = [];
    
    // Validate age
    const ageField = document.getElementById('age');
    if (ageField) {
        const age = parseInt(ageField.value);
        if (!age || age < 18 || age > 120) {
            isValid = false;
            errors.push('Age must be between 18 and 120');
            markFieldInvalid(ageField);
        } else {
            markFieldValid(ageField);
        }
    }
    
    // Validate gender
    const genderField = document.getElementById('gender');
    if (genderField && !genderField.value) {
        isValid = false;
        errors.push('Please select your gender');
        markFieldInvalid(genderField);
    } else if (genderField) {
        markFieldValid(genderField);
    }
    
    // Validate income
    const incomeField = document.getElementById('total_income');
    if (incomeField) {
        const income = parseFloat(incomeField.value);
        if (!income || income < 0) {
            isValid = false;
            errors.push('Total income must be a positive number');
            markFieldInvalid(incomeField);
        } else {
            markFieldValid(incomeField);
        }
    }
    
    // Validate that at least one expense category is selected
    const expenseCategories = [
        'utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare'
    ];
    
    let hasExpenses = false;
    expenseCategories.forEach(category => {
        const checkbox = document.getElementById(`${category}_check`);
        const amountField = document.getElementById(`${category}_amount`);
        
        if (checkbox && checkbox.checked) {
            hasExpenses = true;
            const amount = parseFloat(amountField.value);
            if (!amount || amount < 0) {
                isValid = false;
                errors.push(`Please enter a valid amount for ${category.replace('_', ' ')}`);
                markFieldInvalid(amountField);
            } else {
                markFieldValid(amountField);
            }
        }
    });
    
    if (!hasExpenses) {
        isValid = false;
        errors.push('Please select at least one expense category');
    }
    
    return isValid;
}

function validateField(field) {
    const fieldId = field.id;
    let isValid = true;
    
    switch (fieldId) {
        case 'age':
            const age = parseInt(field.value);
            isValid = age && age >= 18 && age <= 120;
            break;
        case 'gender':
            isValid = field.value !== '';
            break;
        case 'total_income':
            const income = parseFloat(field.value);
            isValid = income && income >= 0;
            break;
        default:
            if (field.classList.contains('expense-amount')) {
                const amount = parseFloat(field.value);
                isValid = !field.value || (amount && amount >= 0);
            }
            break;
    }
    
    if (isValid) {
        markFieldValid(field);
    } else {
        markFieldInvalid(field);
    }
    
    return isValid;
}

function markFieldValid(field) {
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
    
    // Remove any existing error messages
    const errorDiv = field.parentElement.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function markFieldInvalid(field, message = '') {
    field.classList.remove('is-valid');
    field.classList.add('is-invalid');
    
    // Add error message if provided
    if (message) {
        let errorDiv = field.parentElement.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentElement.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }
}

function showValidationErrors() {
    // Scroll to first invalid field
    const firstInvalidField = document.querySelector('.is-invalid');
    if (firstInvalidField) {
        firstInvalidField.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
        firstInvalidField.focus();
    }
}

// Add smooth animations for better UX
function addFadeInClass(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'all 0.3s ease';
    
    setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 100);
}

// Initialize tooltips if Bootstrap is available
if (typeof bootstrap !== 'undefined') {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Export functions for testing or external use
window.SurveyFormUtils = {
    calculateTotalExpenses,
    validateForm,
    formatCurrency
};