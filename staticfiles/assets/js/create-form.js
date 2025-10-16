/**
 * Create Request Form - Optimized JavaScript
 * Focused on UX essentials only
 */

let currentStep = 1;
const totalSteps = 4; // Step 1, 2, 3, 4

// Initialize form when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM Loaded - Initializing create form');
    initializeForm();
    setupValidation();
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
    
    // Setup file input listeners
    setupFileInputListeners();
    
    console.log('✅ Form initialized');
}

// Setup file input listeners (essential for UX)
function setupFileInputListeners() {
    console.log('🔧 Setting up file input listeners...');
    
    // Emirates ID image input
    const idImageInput = document.getElementById('idImage');
    if (idImageInput) {
        idImageInput.addEventListener('change', function() {
            console.log('📁 ID Image input changed');
            handleIdImageUpload();
            validateIdImageUpload();
        });
    }
    
    // Additional documents input
    const additionalDocsInput = document.getElementById('additionalDocs');
    if (additionalDocsInput) {
        additionalDocsInput.addEventListener('change', function() {
            console.log('📁 Additional docs input changed');
            handleAdditionalDocsUpload();
        });
    }
    
    console.log('✅ File input listeners setup complete');
}

// Handle Emirates ID image upload (essential for UX)
function handleIdImageUpload() {
    const idImageInput = document.getElementById('idImage');
    const idImagePreview = document.getElementById('idImagePreview');
    
    if (!idImageInput || !idImagePreview) return;
    
    const file = idImageInput.files[0];
    if (file) {
        console.log('📸 Processing Emirates ID image:', file.name);
        
        const reader = new FileReader();
        reader.onload = function(e) {
            idImagePreview.innerHTML = `
                <img src="${e.target.result}" alt="Emirates ID Preview" class="img-thumbnail">
                <div class="mt-2">
                    <small class="text-success">
                        <i class="fas fa-check-circle"></i>
                        ${file.name}
                    </small>
                </div>
            `;
        };
        reader.readAsDataURL(file);
    } else {
        idImagePreview.innerHTML = '';
    }
}

// Handle additional documents upload (essential for UX)
function handleAdditionalDocsUpload() {
    const additionalDocsInput = document.getElementById('additionalDocs');
    const additionalDocsPreview = document.getElementById('additionalDocsPreview');
    
    if (!additionalDocsInput || !additionalDocsPreview) return;
    
    const files = Array.from(additionalDocsInput.files);
    if (files.length > 0) {
        console.log('📄 Processing additional documents:', files.length);
        
        let previewHTML = '';
        files.forEach((file, index) => {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewHTML += `
                        <div class="d-inline-block me-2 mb-2">
                            <img src="${e.target.result}" alt="${file.name}" class="img-thumbnail" style="max-width: 80px; max-height: 80px;">
                            <div class="small text-center mt-1">${file.name.length > 15 ? file.name.substring(0, 15) + '...' : file.name}</div>
                        </div>
                    `;
                    additionalDocsPreview.innerHTML = previewHTML;
                };
                reader.readAsDataURL(file);
            } else {
                previewHTML += `
                    <div class="d-inline-block me-2 mb-2 text-center">
                        <i class="fas ${getFileIcon(file.name)} fa-2x text-primary"></i>
                        <div class="small mt-1">${file.name.length > 15 ? file.name.substring(0, 15) + '...' : file.name}</div>
                    </div>
                `;
                additionalDocsPreview.innerHTML = previewHTML;
            }
        });
    } else {
        additionalDocsPreview.innerHTML = '';
    }
}

// Function to get file icon (essential for UX)
function getFileIcon(filename) {
    const extension = filename.split('.').pop().toLowerCase();
    switch(extension) {
        case 'pdf':
            return 'fa-file-pdf text-danger';
        case 'doc':
        case 'docx':
            return 'fa-file-word text-primary';
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
            return 'fa-file-image text-success';
        case 'xls':
        case 'xlsx':
            return 'fa-file-excel text-success';
        case 'zip':
        case 'rar':
            return 'fa-file-archive text-warning';
        default:
            return 'fa-file-alt text-secondary';
    }
}

// Real-time validation for ID image upload (essential for UX)
function validateIdImageUpload() {
    const idImageInput = document.getElementById('idImage');
    const idImageUpload = document.getElementById('idImageUpload');
    
    if (!idImageInput || !idImageUpload) return;
    
    if (idImageInput.files && idImageInput.files.length > 0) {
        console.log('✅ ID Image uploaded - removing error styling');
        
        // Remove error styling
        idImageUpload.classList.remove('border-danger');
        idImageUpload.classList.add('border-success');
        idImageUpload.style.borderColor = '#28a745';
        idImageUpload.style.borderWidth = '2px';
        idImageUpload.style.borderStyle = 'solid';
        
        // Remove error message
        const errorMsg = document.getElementById('idImageError');
        if (errorMsg) {
            errorMsg.remove();
        }
    } else {
        console.log('❌ ID Image not uploaded - adding error styling');
        
        // Add error styling
        idImageUpload.classList.remove('border-success');
        idImageUpload.classList.add('border-danger');
        idImageUpload.style.borderColor = '#dc3545';
        idImageUpload.style.borderWidth = '2px';
        idImageUpload.style.borderStyle = 'solid';
        
        // Add error message
        const errorMsg = document.getElementById('idImageError') || createErrorMessage('idImageUpload', 'يرجى رفع صورة الهوية الإماراتية');
    }
}

// ============ STEP NAVIGATION ============

function changeStep(direction) {
    console.log(`🔄 Changing step: ${currentStep} + ${direction}`);
    
    if (direction > 0 && !validateCurrentStep()) {
        console.log('❌ Current step validation failed');
        return false;
    }
    
    if (direction > 0) {
        if (currentStep < totalSteps) {
            currentStep++;
        }
    } else if (direction < 0) {
        if (currentStep > 1) {
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
        const isCurrentStep = stepNumber === currentStep;
        step.classList.toggle('d-none', !isCurrentStep);
    });
    
    // Update step numbers
    const stepNumbers = document.querySelectorAll('.step-number');
    stepNumbers.forEach((number, index) => {
        const stepNumber = index + 1;
        const isCompleted = stepNumber <= currentStep;
        
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

// ============ VALIDATION (Essential for UX) ============

function setupValidation() {
    // Name matching (essential for UX)
    const nameInput = document.getElementById('customerName');
    const confirmInput = document.getElementById('confirmName');
    if (nameInput && confirmInput) {
        nameInput.addEventListener('input', checkNameMatch);
        confirmInput.addEventListener('input', checkNameMatch);
    }
    
    // Emirates ID validation (essential for UX)
    const idInput = document.getElementById('emiratesId');
    if (idInput) {
        idInput.addEventListener('input', validateEmiratesId);
    }
    
    // Date of birth validation (essential for UX)
    const dobInput = document.getElementById('dateOfBirth');
    if (dobInput) {
        dobInput.addEventListener('change', validateDateOfBirth);
    }
    
    // Documents validation
    const idImageInput = document.getElementById('idImage');
    if (idImageInput) {
        idImageInput.addEventListener('change', checkDocumentsUpload);
    }
    
    // Payment methods (essential for UX)
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
}

function validateCurrentStep() {
    console.log(`🔍 Validating step ${currentStep}...`);
    
    switch (currentStep) {
        case 1:
            return validateStep1();
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
    
    console.log(`✅ Step 1 validation: ${isValid ? 'PASSED' : 'FAILED'}`);
    return isValid;
}

function validateStep2() {
    console.log('🔍 Validating Step 2 (Documents)...');
    
    // التحقق من رفع صورة الهوية الإماراتية (إجباري)
    const idImageInput = document.getElementById('idImage');
    let isValid = true;
    
    if (!idImageInput || !idImageInput.files || idImageInput.files.length === 0) {
        console.log('❌ Missing Emirates ID image upload');
        validateIdImageUpload();
        isValid = false;
    } else {
        console.log('✅ Emirates ID image uploaded');
        validateIdImageUpload();
    }
    
    console.log(`✅ Step 2 validation: ${isValid ? 'PASSED' : 'FAILED'}`);
    return isValid;
}


function validateStep4() {
    console.log('🔍 Validating Step 4...');
    
    const paymentMethod = document.querySelector('input[name="paymentMethod"]:checked');
    console.log('💳 Payment method selected:', paymentMethod?.value);
    
    if (!paymentMethod) {
        console.log('❌ No payment method selected - setting default to paytabs');
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
            if (receiptNumber) {
                receiptNumber.classList.add('is-invalid');
                receiptNumber.classList.remove('is-valid');
            }
            return false;
        } else {
            if (receiptNumber) {
                receiptNumber.classList.remove('is-invalid');
                receiptNumber.classList.add('is-valid');
            }
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

// ============ VALIDATION HELPERS (Essential for UX) ============

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

function checkDocumentsUpload() {
    const idImageInput = document.getElementById('idImage');
    const checkbox = document.getElementById('checkDocuments');
    
    if (idImageInput && idImageInput.files && idImageInput.files.length > 0 && checkbox) {
        checkbox.checked = true;
        checkbox.disabled = false;
        updateProgressBar();
    } else if (checkbox) {
        checkbox.checked = false;
        checkbox.disabled = true;
    }
}

// دالة مساعدة لإنشاء رسائل الخطأ
function createErrorMessage(parentId, message) {
    const parent = document.getElementById(parentId);
    if (!parent) return null;
    
    // إزالة رسالة الخطأ الموجودة
    const existingError = document.getElementById(parentId + 'Error');
    if (existingError) {
        existingError.remove();
    }
    
    // إنشاء رسالة خطأ جديدة
    const errorDiv = document.createElement('div');
    errorDiv.id = parentId + 'Error';
    errorDiv.className = 'form-text text-danger mt-2';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-1"></i>${message}`;
    
    parent.appendChild(errorDiv);
    return errorDiv;
}

// ============ PROGRESS & CHECKLIST (Essential for UX) ============

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
    const currentStepChecks = document.getElementById(`step${currentStep}Checks`);
    
    if (currentStepChecks) {
        currentStepChecks.classList.remove('d-none');
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
    
    // Handle template (auto-selected by system)
    const reviewAuthType = document.getElementById('reviewAuthType');
    const reviewVersion = document.getElementById('reviewVersion');
    if (reviewAuthType) {
        reviewAuthType.textContent = 'سيتم اختياره تلقائياً';
    }
    if (reviewVersion) {
        reviewVersion.textContent = 'تلقائي';
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

// ============ PAYMENT DETAILS (Simplified) ============

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

// ============ FORM SUBMISSION ============

function setupFormSubmission() {
    const form = document.getElementById('createRequestForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('🚀 FORM SUBMISSION EVENT TRIGGERED');
            
            // If we're not on the last step, prevent submission and go to next step
            if (currentStep < totalSteps) {
                console.log('⚠️ Not on last step - preventing submission and going to next step');
                e.preventDefault();
                changeStep(1);
                return false;
            }
            
            // We're on the last step - validate and submit
            console.log('✅ On last step - validating and submitting');
            
            const validationResult = validateStep4();
            console.log('🔍 Validation result:', validationResult);
            
            if (!validationResult) {
                console.log('❌ Final step validation failed - preventing submission');
                e.preventDefault();
                return false;
            }
            
            console.log('✅ All validation passed - submitting to Django');
            console.log('✅ Form will be submitted to:', form.action);
            
            // Don't prevent default - let Django handle the form submission
            console.log('✅ Allowing form submission to proceed...');
        });
    } else {
        console.error('❌ Form not found!');
    }
}
