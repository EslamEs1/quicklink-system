/**
 * Create Request Form - Fixed JavaScript
 * Enhanced debugging and validation
 */

let currentStep = 1;
const totalSteps = 5; // Step 1, 1.5, 2, 3, 4

// Initialize form when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM Loaded - Initializing create form');
    initializeForm();
    setupValidation();
    setupAutoSave();
    loadSavedData();
    setupFormSubmission();
});

// ============ INITIALIZATION ============

function initializeForm() {
    console.log('🔧 Initializing form...');
    
    // Set today's date
    const today = new Date();
    const dateInput = document.getElementById('requestDate');
    if (dateInput) {
        dateInput.value = today.toISOString().split('T')[0];
    }
    
    // Generate reference number
    const referenceInput = document.getElementById('referenceNumber');
    if (referenceInput && !referenceInput.value) {
        const year = today.getFullYear();
        const timestamp = Date.now().toString().slice(-6); // Last 6 digits
        referenceInput.value = `QL-${year}-${timestamp}`;
        console.log('✅ Reference number generated:', referenceInput.value);
    }
    
    // Set date of birth constraints
    const dobInput = document.getElementById('dateOfBirth');
    if (dobInput) {
        const maxDate = new Date(today);
        maxDate.setFullYear(today.getFullYear() - 7); // 7 years back
        
        const minDate = new Date(today);
        minDate.setFullYear(today.getFullYear() - 120); // 120 years back
        
        dobInput.setAttribute('max', maxDate.toISOString().split('T')[0]);
        dobInput.setAttribute('min', minDate.toISOString().split('T')[0]);
    }
    
    console.log('✅ Form initialized');
}

// ============ STEP NAVIGATION ============

function changeStep(direction) {
    console.log(`🔄 Changing step: ${currentStep} + ${direction}`);
    
    if (direction > 0 && !validateCurrentStep()) {
        console.log('❌ Current step validation failed');
        return false;
    }
    
    if (direction > 0) {
        if (currentStep === 1) {
            currentStep = 1.5; // Go to document upload step
        } else if (currentStep === 1.5) {
            currentStep = 2; // Go to template selection
        } else if (currentStep < totalSteps) {
            currentStep++;
        }
    } else if (direction < 0) {
        if (currentStep === 2) {
            currentStep = 1.5; // Go back to document upload
        } else if (currentStep === 1.5) {
            currentStep = 1; // Go back to customer data
        } else if (currentStep > 1) {
            currentStep--;
        }
    }
    
    console.log(`✅ New step: ${currentStep}`);
    
    updateStepDisplay();
    updateButtons();
    
    if (currentStep === 3) {
        updateReviewData();
    } else if (currentStep === 4) {
        updatePaymentDetails();
    }
}

function updateStepDisplay() {
    // Update step content
    const steps = document.querySelectorAll('.step-content');
    steps.forEach((step, index) => {
        const stepNumber = index + 1;
        // Step 1.5 is index 1 (second element)
        const isCurrentStep = (currentStep === 1.5 && stepNumber === 2) || 
                             (currentStep !== 1.5 && stepNumber === currentStep);
        step.classList.toggle('d-none', !isCurrentStep);
    });
    
    // Update step numbers
    const stepNumbers = document.querySelectorAll('.step-number');
    stepNumbers.forEach((number, index) => {
        const stepNumber = index + 1;
        const isCompleted = (currentStep > 1.5 && stepNumber <= 2) || 
                           (currentStep === 1.5 && stepNumber <= 2) ||
                           (currentStep < 1.5 && stepNumber <= currentStep);
        
        if (isCompleted) {
            number.classList.add('bg-primary', 'text-white');
            number.classList.remove('bg-light');
        } else {
            number.classList.remove('bg-primary', 'text-white');
            number.classList.add('bg-light');
        }
    });
    
    // Update checklist
    updateChecklistDisplay();
    updateProgressBar();
}

function updateButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    if (prevBtn) {
        prevBtn.style.display = currentStep > 1 ? 'inline-block' : 'none';
    }
    
    if (nextBtn && submitBtn) {
        if (currentStep === totalSteps) {
            nextBtn.classList.add('d-none');
            submitBtn.classList.remove('d-none');
            console.log('✅ Submit button shown');
        } else {
            nextBtn.classList.remove('d-none');
            submitBtn.classList.add('d-none');
        }
    }
}

// ============ VALIDATION ============

function setupValidation() {
    // Name matching
    const nameInput = document.getElementById('customerName');
    const confirmInput = document.getElementById('confirmName');
    if (nameInput && confirmInput) {
        nameInput.addEventListener('input', checkNameMatch);
        confirmInput.addEventListener('input', checkNameMatch);
    }
    
    // Emirates ID validation
    const idInput = document.getElementById('emiratesId');
    if (idInput) {
        idInput.addEventListener('input', validateEmiratesId);
    }
    
    // Date of birth validation
    const dobInput = document.getElementById('dateOfBirth');
    if (dobInput) {
        dobInput.addEventListener('change', validateDateOfBirth);
    }
    
    // Template selection
    const templateSelect = document.getElementById('templateSelect');
    if (templateSelect) {
        templateSelect.addEventListener('change', checkTemplateSelection);
    }
    
    // Payment methods
    const paymentMethods = document.querySelectorAll('input[name="paymentMethod"]');
    paymentMethods.forEach(method => {
        method.addEventListener('change', function() {
            console.log('💳 Payment method changed to:', this.value);
            const cashReceipt = document.getElementById('cashReceipt');
            if (cashReceipt) {
                if (this.value === 'cash') {
                    cashReceipt.classList.remove('d-none');
                } else {
                    cashReceipt.classList.add('d-none');
                }
            }
            updateProgressBar();
        });
    });
    
    // Image upload is now handled in create.html inline JavaScript
}

function validateCurrentStep() {
    console.log(`🔍 Validating step ${currentStep}...`);
    
    switch (currentStep) {
        case 1:
            return validateStep1();
        case 1.5:
            return validateStep1_5();
        case 2:
            return validateStep2();
        case 3:
            return true; // Review step
        case 4:
            return validateStep4();
        default:
            return false;
    }
}

function validateStep1() {
    console.log('🔍 Validating Step 1...');
    const required = ['customerName', 'confirmName', 'emiratesId', 'dateOfBirth', 'nationality', 'mobileNumber', 'requestType'];
    let isValid = true;
    
    // التحقق من الحقول المطلوبة
    required.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field || !field.value.trim()) {
            console.log(`❌ Missing field: ${fieldId}`);
            if (field) field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // لا نحتاج للتحقق من رفع الصورة هنا لأنها أصبحت في Step 1.5
    
    console.log(`✅ Step 1 validation: ${isValid ? 'PASSED' : 'FAILED'}`);
    return isValid;
}

function validateStep1_5() {
    console.log('🔍 Validating Step 1.5 (Documents)...');
    
    // التحقق من رفع صورة الهوية الإماراتية (إجباري)
    const idImageInput = document.getElementById('idImage');
    let isValid = true;
    
    if (!idImageInput || !idImageInput.files || idImageInput.files.length === 0) {
        console.log('❌ Missing Emirates ID image upload');
        isValid = false;
    } else {
        console.log('✅ Emirates ID image uploaded');
    }
    
    // المستندات الإضافية اختيارية، لا نحتاج للتحقق منها
    
    console.log(`✅ Step 1.5 validation: ${isValid ? 'PASSED' : 'FAILED'}`);
    return isValid;
}

function validateStep2() {
    console.log('🔍 Validating Step 2...');
    const templateSelect = document.getElementById('templateSelect');
    
    if (!templateSelect || !templateSelect.value) {
        console.log('❌ No template selected');
        if (templateSelect) {
            templateSelect.classList.add('is-invalid');
        }
        return false;
    }
    
    templateSelect.classList.remove('is-invalid');
    console.log('✅ Step 2 validation: PASSED');
    return true;
}

function validateStep4() {
    console.log('🔍 Validating Step 4...');
    
    const paymentMethod = document.querySelector('input[name="paymentMethod"]:checked');
    console.log('💳 Payment method selected:', paymentMethod?.value);
    
    if (!paymentMethod) {
        console.log('❌ No payment method selected - setting default to paytabs');
        // Set default to paytabs if none selected
        const paytabsRadio = document.getElementById('paytabs');
        if (paytabsRadio) {
            paytabsRadio.checked = true;
            console.log('✅ Set default payment method to paytabs');
        } else {
            console.log('❌ Paytabs radio button not found');
            return false;
        }
    }
    
    const finalPaymentMethod = document.querySelector('input[name="paymentMethod"]:checked');
    if (finalPaymentMethod && finalPaymentMethod.value === 'cash') {
        const receiptNumber = document.getElementById('receiptNumber');
        console.log('💵 Cash payment - checking receipt number');
        if (!receiptNumber || !receiptNumber.value.trim()) {
            console.log('❌ Cash payment but no receipt number');
            return false;
        }
    }
    
    console.log('✅ Step 4 validation: PASSED');
    return true;
}

// ============ CUSTOMER FORM TOGGLE ============

function toggleCustomerForm() {
    const existingOption = document.getElementById('existingCustomer');
    const existingSection = document.getElementById('existingCustomerSection');
    const newSection = document.getElementById('newCustomerSection');
    
    if (existingOption && existingOption.checked) {
        existingSection?.classList.remove('d-none');
        newSection?.classList.add('d-none');
    } else {
        existingSection?.classList.add('d-none');
        newSection?.classList.remove('d-none');
    }
}

function selectExistingCustomer(id, name, emirates_id, phone, email) {
    const hiddenInput = document.getElementById('existingCustomerId');
    const alertDiv = document.getElementById('selectedCustomerAlert');
    const nameSpan = document.getElementById('selectedCustomerName');
    
    if (hiddenInput) hiddenInput.value = id;
    if (nameSpan) nameSpan.textContent = name;
    if (alertDiv) alertDiv.classList.remove('d-none');
    
    // Highlight selected customer
    document.querySelectorAll('#customerSearchResults .list-group-item').forEach(item => {
        item.classList.remove('active');
    });
    event.target.closest('.list-group-item')?.classList.add('active');
}

// ============ VALIDATION HELPERS ============

function checkNameMatch() {
    const name = document.getElementById('customerName')?.value || '';
    const confirmName = document.getElementById('confirmName')?.value || '';
    const errorDiv = document.getElementById('nameMatchError');
    const successDiv = document.getElementById('nameMatchSuccess');
    const checkbox = document.getElementById('checkName');
    
    if (name && confirmName) {
        if (name === confirmName) {
            if (errorDiv) errorDiv.style.display = 'none';
            if (successDiv) successDiv.style.display = 'block';
            if (checkbox) {
                checkbox.checked = true;
                checkbox.disabled = false;
            }
        } else {
            if (errorDiv) errorDiv.style.display = 'block';
            if (successDiv) successDiv.style.display = 'none';
            if (checkbox) {
                checkbox.checked = false;
                checkbox.disabled = true;
            }
        }
    } else {
        if (errorDiv) errorDiv.style.display = 'none';
        if (successDiv) successDiv.style.display = 'none';
        if (checkbox) {
            checkbox.checked = false;
            checkbox.disabled = true;
        }
    }
    updateProgressBar();
}

function validateEmiratesId() {
    const idInput = document.getElementById('emiratesId');
    const id = idInput?.value?.trim() || '';
    const errorDiv = document.getElementById('idFormatError');
    const successDiv = document.getElementById('idFormatSuccess');
    const checkbox = document.getElementById('checkId');
    
    const idPattern = /^784-\d{4}-\d{7}-\d{1}$/;
    
    if (id) {
        if (idPattern.test(id)) {
            if (errorDiv) errorDiv.style.display = 'none';
            if (successDiv) successDiv.style.display = 'block';
            if (checkbox) {
                checkbox.checked = true;
                checkbox.disabled = false;
            }
            idInput.classList.remove('is-invalid');
            idInput.classList.add('is-valid');
        } else {
            if (errorDiv) errorDiv.style.display = 'block';
            if (successDiv) successDiv.style.display = 'none';
            if (checkbox) {
                checkbox.checked = false;
                checkbox.disabled = true;
            }
            idInput.classList.remove('is-valid');
            idInput.classList.add('is-invalid');
        }
    } else {
        if (errorDiv) errorDiv.style.display = 'none';
        if (successDiv) successDiv.style.display = 'none';
        if (checkbox) {
            checkbox.checked = false;
            checkbox.disabled = true;
        }
        idInput?.classList.remove('is-valid', 'is-invalid');
    }
    updateProgressBar();
}

function validateDateOfBirth() {
    const dobInput = document.getElementById('dateOfBirth');
    const dob = new Date(dobInput?.value || '');
    const today = new Date();
    const errorDiv = document.getElementById('dobError');
    const errorMsg = document.getElementById('dobErrorMsg');
    const successDiv = document.getElementById('dobSuccess');
    const ageDisplay = document.getElementById('ageDisplay');
    
    if (!dobInput?.value) {
        if (errorDiv) errorDiv.style.display = 'none';
        if (successDiv) successDiv.style.display = 'none';
        dobInput?.classList.remove('is-valid', 'is-invalid');
        return;
    }
    
    // Calculate age
    let age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
        age--;
    }
    
    if (dob > today) {
        if (errorMsg) errorMsg.textContent = 'لا يمكن اختيار تاريخ من المستقبل!';
        if (errorDiv) errorDiv.style.display = 'block';
        if (successDiv) successDiv.style.display = 'none';
        dobInput.classList.remove('is-valid');
        dobInput.classList.add('is-invalid');
    } else if (age < 7) {
        if (errorMsg) errorMsg.textContent = `العمر ${age} سنوات - يجب أن يكون 7 سنوات على الأقل`;
        if (errorDiv) errorDiv.style.display = 'block';
        if (successDiv) successDiv.style.display = 'none';
        dobInput.classList.remove('is-valid');
        dobInput.classList.add('is-invalid');
    } else if (age > 120) {
        if (errorMsg) errorMsg.textContent = `العمر ${age} سنة - يرجى التحقق من التاريخ`;
        if (errorDiv) errorDiv.style.display = 'block';
        if (successDiv) successDiv.style.display = 'none';
        dobInput.classList.remove('is-valid');
        dobInput.classList.add('is-invalid');
    } else {
        if (ageDisplay) ageDisplay.textContent = age;
        if (errorDiv) errorDiv.style.display = 'none';
        if (successDiv) successDiv.style.display = 'block';
        dobInput.classList.remove('is-invalid');
        dobInput.classList.add('is-valid');
    }
}

function checkTemplateSelection() {
    const templateSelect = document.getElementById('templateSelect');
    const checkbox = document.getElementById('checkTemplate');
    
    if (templateSelect && templateSelect.value && checkbox) {
        checkbox.checked = true;
        checkbox.disabled = false;
        updateProgressBar();
    } else if (checkbox) {
        checkbox.checked = false;
        checkbox.disabled = true;
    }
}

// ============ IMAGE UPLOAD ============
// Image upload is now handled in create.html inline JavaScript

// ============ PROGRESS & CHECKLIST ============

function updateChecklistDisplay() {
    const currentStepNum = document.getElementById('currentStepNum');
    if (currentStepNum) {
        currentStepNum.textContent = currentStep;
    }
    
    // Hide all step checks
    for (let i = 1; i <= 4; i++) {
        const stepChecks = document.getElementById(`step${i}Checks`);
        if (stepChecks) {
            stepChecks.classList.add('d-none');
        }
    }
    
    // Show current step checks
    let currentStepChecks;
    if (currentStep === 1.5) {
        currentStepChecks = document.getElementById('step1_5Checks');
    } else {
        currentStepChecks = document.getElementById(`step${currentStep}Checks`);
    }
    
    if (currentStepChecks) {
        currentStepChecks.classList.remove('d-none');
    }
    
    // Hide/show image upload card (removed since we moved to step 1.5)
    const imageCard = document.getElementById('imageUploadCard');
    if (imageCard) {
        imageCard.classList.add('d-none'); // Always hide since we moved to step 1.5
    }
}

function updateProgressBar() {
    const allCheckboxes = document.querySelectorAll('#checklistCard input[type="checkbox"]');
    let totalChecks = 0;
    let completedChecks = 0;
    
    allCheckboxes.forEach(checkbox => {
        totalChecks++;
        if (checkbox.checked) {
            completedChecks++;
        }
    });
    
    const percentage = totalChecks > 0 ? Math.round((completedChecks / totalChecks) * 100) : 0;
    const progressBar = document.getElementById('progressBar');
    
    if (progressBar) {
        progressBar.style.width = percentage + '%';
        progressBar.textContent = percentage + '%';
        
        progressBar.className = 'progress-bar';
        if (percentage < 33) {
            progressBar.classList.add('bg-danger');
        } else if (percentage < 66) {
            progressBar.classList.add('bg-warning');
        } else {
            progressBar.classList.add('bg-success');
        }
    }
}

// ============ REVIEW DATA ============

function updateReviewData() {
    const fields = {
        'reviewName': 'customerName',
        'reviewId': 'emiratesId',
        'reviewBirth': 'dateOfBirth',
        'reviewMobile': 'mobileNumber',
        'reviewEmail': 'email',
        'reviewReference': 'referenceNumber'
    };
    
    Object.entries(fields).forEach(([reviewId, inputId]) => {
        const reviewElement = document.getElementById(reviewId);
        const inputElement = document.getElementById(inputId);
        if (reviewElement && inputElement) {
            reviewElement.textContent = inputElement.value || '-';
        }
    });
    
    // Handle nationality
    const nationalitySelect = document.getElementById('nationality');
    const reviewNationality = document.getElementById('reviewNationality');
    if (reviewNationality && nationalitySelect) {
        reviewNationality.textContent = nationalitySelect.options[nationalitySelect.selectedIndex]?.text || '-';
    }
    
    // Handle request type
    const requestTypeSelect = document.getElementById('requestType');
    const reviewType = document.getElementById('reviewType');
    if (reviewType && requestTypeSelect) {
        reviewType.textContent = requestTypeSelect.options[requestTypeSelect.selectedIndex]?.text || '-';
    }
    
    // Handle template
    const templateSelect = document.getElementById('templateSelect');
    const reviewAuthType = document.getElementById('reviewAuthType');
    const reviewVersion = document.getElementById('reviewVersion');
    if (templateSelect) {
        if (reviewAuthType) {
            reviewAuthType.textContent = templateSelect.value ? 
                templateSelect.options[templateSelect.selectedIndex]?.text || '-' : 'لم يتم الاختيار';
        }
        if (reviewVersion) {
            reviewVersion.textContent = templateSelect.options[templateSelect.selectedIndex]?.getAttribute('data-version') || '-';
        }
    }
    
    // Handle request date
    const requestDate = document.getElementById('requestDate');
    const reviewDate = document.getElementById('reviewDate');
    if (reviewDate && requestDate) {
        reviewDate.textContent = requestDate.value || '-';
    }
    
    // Handle image
    const imageInput = document.getElementById('idImage');
    const reviewImage = document.getElementById('reviewImage');
    if (reviewImage && imageInput) {
        reviewImage.textContent = imageInput.files.length ? 'تم الرفع' : 'لم يتم الرفع';
    }
}

// ============ PAYMENT DETAILS ============

function updatePaymentDetails() {
    const requestTypeSelect = document.getElementById('requestType');
    
    if (!requestTypeSelect || !requestTypeSelect.value) {
        document.getElementById('serviceName').textContent = 'لم يتم اختيار نوع الخدمة';
        document.getElementById('servicePrice').textContent = '0 درهم';
        document.getElementById('taxAmount').textContent = '0 درهم';
        document.getElementById('totalAmount').textContent = '0 درهم';
        return;
    }
    
    const selectedOption = requestTypeSelect.options[requestTypeSelect.selectedIndex];
    const serviceName = selectedOption.text.split(' - ')[0];
    const basePrice = parseFloat(selectedOption.getAttribute('data-price')) || 0;
    const taxAmount = basePrice * 0.05;
    const totalAmount = basePrice + taxAmount;
    
    document.getElementById('serviceName').textContent = serviceName;
    document.getElementById('servicePrice').textContent = basePrice.toFixed(2) + ' درهم';
    document.getElementById('taxAmount').textContent = taxAmount.toFixed(2) + ' درهم';
    document.getElementById('totalAmount').textContent = totalAmount.toFixed(2) + ' درهم';
}

// ============ AUTO-SAVE ============

function setupAutoSave() {
    const inputs = document.querySelectorAll('#createRequestForm input, #createRequestForm select');
    inputs.forEach(input => {
        input.addEventListener('change', saveFormData);
        input.addEventListener('input', debounce(saveFormData, 1000));
    });
    
    window.addEventListener('beforeunload', saveFormData);
}

function saveFormData() {
    const formData = {
        currentStep: currentStep,
        customerName: document.getElementById('customerName')?.value || '',
        confirmName: document.getElementById('confirmName')?.value || '',
        emiratesId: document.getElementById('emiratesId')?.value || '',
        dateOfBirth: document.getElementById('dateOfBirth')?.value || '',
        nationality: document.getElementById('nationality')?.value || '',
        mobileNumber: document.getElementById('mobileNumber')?.value || '',
        email: document.getElementById('email')?.value || '',
        requestType: document.getElementById('requestType')?.value || '',
        priority: document.getElementById('priority')?.value || '',
        dueDate: document.getElementById('dueDate')?.value || '',
        templateSelect: document.getElementById('templateSelect')?.value || '',
        paymentMethod: document.querySelector('input[name="paymentMethod"]:checked')?.value || '',
        timestamp: new Date().toISOString()
    };
    
    localStorage.setItem('createRequestFormData', JSON.stringify(formData));
}

function loadSavedData() {
    const savedData = localStorage.getItem('createRequestFormData');
    if (!savedData) return;
    
    try {
        const formData = JSON.parse(savedData);
        const savedTime = new Date(formData.timestamp);
        const now = new Date();
        const minutesDiff = (now - savedTime) / (1000 * 60);
        
        // Only restore if data is between 1-5 minutes old
        if (minutesDiff > 5 || minutesDiff < 1) {
            localStorage.removeItem('createRequestFormData');
            return;
        }
        
        const hasData = formData.customerName || formData.emiratesId || formData.email || formData.mobileNumber;
        if (!hasData) {
            localStorage.removeItem('createRequestFormData');
            return;
        }
        
        if (confirm('تم العثور على بيانات محفوظة منذ ' + Math.round(minutesDiff) + ' دقيقة. هل تريد استعادتها؟')) {
            // Restore form data
            Object.entries(formData).forEach(([key, value]) => {
                if (key === 'paymentMethod') {
                    const paymentRadio = document.getElementById(value);
                    if (paymentRadio) paymentRadio.checked = true;
                } else if (key === 'currentStep' && value > 1) {
                    currentStep = value;
                    changeStep(0);
                } else if (key !== 'timestamp') {
                    const element = document.getElementById(key);
                    if (element) element.value = value;
                }
            });
            
            // Re-run validations
            checkNameMatch();
            validateEmiratesId();
            validateDateOfBirth();
        } else {
            localStorage.removeItem('createRequestFormData');
        }
    } catch (error) {
        localStorage.removeItem('createRequestFormData');
    }
}

function clearSavedData() {
    localStorage.removeItem('createRequestFormData');
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============ FORM SUBMISSION ============

function setupFormSubmission() {
    const form = document.getElementById('createRequestForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('🚀 FORM SUBMISSION EVENT TRIGGERED');
            console.log('📝 Current step:', currentStep);
            console.log('📝 Total steps:', totalSteps);
            console.log('📝 Form action:', form.action);
            console.log('📝 Form method:', form.method);
            
            // If we're not on the last step, prevent submission and go to next step
            if (currentStep < totalSteps) {
                console.log('⚠️ Not on last step - preventing submission and going to next step');
                e.preventDefault();
                changeStep(1);
                return false;
            }
            
            // We're on the last step - validate and submit
            console.log('✅ On last step - validating and submitting');
            
            // Validate final step
            console.log('🔍 Starting final validation...');
            const validationResult = validateStep4();
            console.log('🔍 Validation result:', validationResult);
            
            if (!validationResult) {
                console.log('❌ Final step validation failed - preventing submission');
                e.preventDefault();
                return false;
            }
            
            console.log('✅ All validation passed - submitting to Django');
            console.log('✅ Form will be submitted to:', form.action);
            clearSavedData();
            
            // Don't prevent default - let Django handle the form submission
            // Django will redirect to detail page on success
            console.log('✅ Allowing form submission to proceed...');
        });
    } else {
        console.error('❌ Form not found!');
    }
}
