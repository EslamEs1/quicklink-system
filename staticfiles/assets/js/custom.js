/* Quick Link System - Custom JavaScript */

// إعداد تبديل الشريط الجانبي (يتم استدعاؤه بعد تحميل المكونات)
function setupSidebarToggle() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    
    // إخفاء الشريط الجانبي على الشاشات الصغيرة
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('show');
    } else {
        sidebar.classList.add('show');
    }
    
    // إضافة مستمع لحجم الشاشة
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.add('show');
        } else {
            sidebar.classList.remove('show');
        }
    });
}

// تبديل الشريط الجانبي
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}

// إغلاق الشريط الجانبي عند النقر خارجه
document.addEventListener('click', function(e) {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('[onclick="toggleSidebar()"]');
    
    if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('show')) {
        if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
            sidebar.classList.remove('show');
        }
    }
});

// وظائف التهيئة (يتم استدعاؤها بعد تحميل المكونات)
function initializeSystem() {
    // تهيئة التحقق من صحة البيانات
    initializeValidation();
    
    // تهيئة الأرقام المرجعية
    initializeReferenceNumbers();
    
    // تهيئة الشريط الجانبي
    initializeSidebar();
    
    // تهيئة التقويم
    initializeDatePicker();
}

// تهيئة الشريط الجانبي (يتم استدعاؤه بعد تحميل المكونات)
function initializeSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    
    const navLinks = sidebar.querySelectorAll('.nav-link');
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        }
    });
}

// تهيئة التحقق من صحة البيانات
function initializeValidation() {
    // التحقق من رقم الهوية الإماراتية
    const idInput = document.getElementById('emiratesId');
    if (idInput) {
        idInput.addEventListener('input', function() {
            validateEmiratesID(this);
        });
    }
    
    // التحقق من تطابق الأسماء
    const nameInput = document.getElementById('customerName');
    const confirmNameInput = document.getElementById('confirmName');
    
    if (nameInput && confirmNameInput) {
        confirmNameInput.addEventListener('input', function() {
            validateNameMatch(nameInput.value, this.value);
        });
    }
}

// التحقق من صحة رقم الهوية الإماراتية
function validateEmiratesID(input) {
    const id = input.value.replace(/\D/g, ''); // إزالة جميع الأرقام غير الرقمية
    const pattern = /^784\d{12}$/;
    
    if (id.length > 0) {
        if (pattern.test(id)) {
            // تنسيق الرقم
            const formatted = id.replace(/(\d{3})(\d{4})(\d{7})(\d{1})/, '$1-$2-$3-$4');
            input.value = formatted;
            showValidationMessage(input, 'رقم الهوية صحيح', 'success');
            enableCreateDraftButton();
        } else {
            showValidationMessage(input, 'رقم الهوية غير صحيح. يجب أن يبدأ بـ 784 ويتكون من 15 رقم', 'error');
            disableCreateDraftButton();
        }
    } else {
        clearValidationMessage(input);
        disableCreateDraftButton();
    }
}

// التحقق من تطابق الأسماء
function validateNameMatch(name, confirmName) {
    const createButton = document.getElementById('createDraftBtn');
    
    if (name && confirmName) {
        if (name.trim() === confirmName.trim()) {
            showValidationMessage(document.getElementById('confirmName'), 'الأسماء متطابقة', 'success');
            if (document.getElementById('emiratesId').value) {
                enableCreateDraftButton();
            }
        } else {
            showValidationMessage(document.getElementById('confirmName'), 'الأسماء غير متطابقة', 'error');
            disableCreateDraftButton();
        }
    } else {
        clearValidationMessage(document.getElementById('confirmName'));
        disableCreateDraftButton();
    }
}

// إظهار رسالة التحقق
function showValidationMessage(input, message, type) {
    let messageElement = input.parentElement.querySelector('.validation-message');
    
    if (!messageElement) {
        messageElement = document.createElement('div');
        messageElement.className = 'validation-message mt-1';
        input.parentElement.appendChild(messageElement);
    }
    
    messageElement.textContent = message;
    messageElement.className = `validation-message mt-1 text-${type === 'success' ? 'success' : 'danger'}`;
}

// مسح رسالة التحقق
function clearValidationMessage(input) {
    const messageElement = input.parentElement.querySelector('.validation-message');
    if (messageElement) {
        messageElement.remove();
    }
}

// تفعيل زر إنشاء المسودة
function enableCreateDraftButton() {
    const button = document.getElementById('createDraftBtn');
    if (button) {
        button.disabled = false;
        button.classList.remove('btn-secondary');
        button.classList.add('btn-primary');
    }
}

// تعطيل زر إنشاء المسودة
function disableCreateDraftButton() {
    const button = document.getElementById('createDraftBtn');
    if (button) {
        button.disabled = true;
        button.classList.remove('btn-primary');
        button.classList.add('btn-secondary');
    }
}

// توليد رقم مرجعي للطلب
function generateReferenceNumber() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    
    // توليد رقم عشوائي
    const randomNum = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    
    return `QL-${year}-${month}${day}-${randomNum}`;
}

// تهيئة الأرقام المرجعية
function initializeReferenceNumbers() {
    const referenceInputs = document.querySelectorAll('[data-auto-reference]');
    referenceInputs.forEach(input => {
        if (!input.value) {
            input.value = generateReferenceNumber();
        }
    });
}


// عرض الطلب
function viewRequest(id) {
    window.location.href = `/${id}/`;
}

// تعديل الطلب
function editRequest(id) {
    window.location.href = `/${id}/edit/`;
}

// حذف الطلب
function deleteRequest(id) {
    if (confirm('هل أنت متأكد من حذف هذا الطلب؟')) {
        showNotification(`تم حذف الطلب رقم ${id}`, 'success');
        loadRequests();
    }
}

// إظهار التنبيهات
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // إزالة التنبيه تلقائياً بعد 5 ثوان
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// وظائف الدفع
function processPayment(requestId, amount) {
    showConfirm('تأكيد الدفع', `هل تريد معالجة دفع بمبلغ ${amount} درهم؟`, 'success', function() {
        showSuccess('تم تسجيل الدفع بنجاح');
        setTimeout(() => location.reload(), 1500);
    });
}

// وظائف البحث والفلترة
function searchRequests(query) {
    const rows = document.querySelectorAll('#requestsTable tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const matches = text.includes(query.toLowerCase());
        
        row.style.display = matches ? '' : 'none';
    });
}

function filterRequests(status) {
    const rows = document.querySelectorAll('#requestsTable tbody tr');
    
    rows.forEach(row => {
        const statusBadge = row.querySelector('.status-badge');
        const rowStatus = statusBadge ? statusBadge.classList.toString() : '';
        
        if (status === 'all' || rowStatus.includes(status.replace('-', ''))) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}


// وظائف التحقق من الصحة المتقدمة
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// تهيئة التقويم
function initializeDatePicker() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.hasAttribute('data-initialized')) {
            input.setAttribute('data-initialized', 'true');
            input.addEventListener('change', function() {
                if (this.value) {
                    this.classList.add('is-valid');
                }
            });
        }
    });
}

// وظائف الطباعة
function printRequest(requestId) {
    window.print();
}

// تصدير البيانات
function exportToExcel() {
    showNotification('جاري تحميل ملف Excel...', 'info');
}

// وظائف الأمان
function maskSensitiveData(text, type) {
    switch (type) {
        case 'phone':
            return text.replace(/(\d{3})\d{4}(\d{3})/, '$1-****-$2');
        case 'id':
            return text.replace(/(\d{3})\d{4}(\d{7})(\d{1})/, '$1-****-$2-$3');
        default:
            return text;
    }
}

// ========================================
// Navigation Functions (Django URLs)
// ========================================

// Customers
function viewCustomer(id) {
    window.location.href = `/clients/${id}/`;
}

function viewCustomerProfile(id) {
    window.location.href = `/clients/${id}/`;
}

function createRequestForCustomer(customerId) {
    window.location.href = `/create/?customer_id=${customerId}`;
}

function editCustomer(id) {
    window.location.href = `/clients/${id}/edit/`;
}

function addNewCustomer() {
    // الآن إنشاء العميل يتم من خلال إنشاء طلب جديد
    window.location.href = '/create/';
}

// Requests
function viewPendingRequest(id) {
    window.location.href = `/${id}/`;
}

function approveRequest(id) {
    showConfirm('تأكيد الموافقة', 'هل تريد الموافقة على هذا الطلب؟', 'success', function() {
        showSuccess('تمت الموافقة على الطلب بنجاح');
        setTimeout(() => location.reload(), 1500);
    });
}

function rejectRequest(id) {
    showConfirm('تأكيد الرفض', 'هل تريد رفض هذا الطلب؟', 'danger', function() {
        showWarning('تم رفض الطلب');
        setTimeout(() => location.reload(), 1500);
    });
}

// Payments
function processNewPayment() {
    showNotification('سيتم فتح بوابة الدفع قريباً', 'info');
}

function viewPaymentDetails(id) {
    showNotification(`عرض تفاصيل الدفع ${id}`, 'info');
}

// Chat & Communication
function callCustomer(phone) {
    window.location.href = '/chat/';
}

// Templates
function viewTemplate(id) {
    showNotification(`عرض القالب ${id}`, 'info');
}

function useTemplate(id) {
    window.location.href = `/create/?template_id=${id}`;
}

function editTemplate(id) {
    showNotification('تحرير القوالب متاح للمشرف الأعلى فقط', 'warning');
}

function createNewTemplate() {
    showNotification('إنشاء قوالب جديدة متاح للمشرف الأعلى فقط', 'warning');
}

// Audit Trail
function viewAuditTrail(id) {
    window.location.href = `/audit/?request_id=${id}`;
}

function viewAuditDetails(id) {
    showNotification(`عرض تفاصيل العملية ${id}`, 'info');
}

// Users
function viewUserProfile(id) {
    window.location.href = `/accounts/profile/?user_id=${id}`;
}

function editUser(id) {
    showNotification(`تحرير المستخدم ${id}`, 'info');
}

function addNewUser() {
    showNotification('سيتم إضافة صفحة إنشاء مستخدم جديد قريباً', 'info');
}

function manageRoles(id) {
    window.location.href = `/settings/permissions/?user_id=${id}`;
}

// Notifications
function viewNotification(id) {
    showNotification(`عرض الإشعار ${id}`, 'info');
}

function markAsRead(id) {
    showNotification('تم وضع علامة مقروء', 'success');
}

// Filters & Utilities
function clearFilters() {
    location.reload();
}

function clearCustomerFilters() {
    location.reload();
}

function clearPaymentFilters() {
    location.reload();
}

function clearAuditFilters() {
    location.reload();
}

function clearNotificationFilters() {
    location.reload();
}

function clearPendingFilters() {
    location.reload();
}

function clearUserFilters() {
    location.reload();
}

// Export Functions
function exportCustomersToExcel() {
    showNotification('جاري تحميل بيانات العملاء...', 'info');
}

function exportPaymentsToExcel() {
    showNotification('جاري تحميل بيانات المدفوعات...', 'info');
}

function exportUsersToExcel() {
    showNotification('جاري تحميل بيانات المستخدمين...', 'info');
}

function exportAuditLog() {
    showNotification('جاري تحميل سجل التدقيق...', 'info');
}

function exportConflicts() {
    showNotification('جاري تحميل تقرير التعارضات...', 'info');
}

// Print Functions
function printRequests() {
    window.print();
}

function printPaymentReport() {
    window.print();
}

function printReceipt(id) {
    window.print();
}

// Backup Functions
function createBackupNow() {
    showConfirm('إنشاء نسخة احتياطية', 'هل تريد إنشاء نسخة احتياطية الآن؟', 'primary', function() {
        showSuccess('جاري إنشاء النسخة الاحتياطية...');
    });
}

function downloadBackup(id) {
    showNotification(`جاري تحميل النسخة الاحتياطية ${id}...`, 'info');
}

function restoreBackup(id) {
    showConfirm('استعادة النسخة الاحتياطية', 'تحذير: سيتم استبدال البيانات الحالية. هل تريد المتابعة؟', 'danger', function() {
        showSuccess('جاري استعادة البيانات...');
    });
}

function deleteBackup(id) {
    showConfirm('حذف النسخة الاحتياطية', 'هل تريد حذف هذه النسخة؟', 'danger', function() {
        showSuccess('تم حذف النسخة الاحتياطية');
    });
}

// Attachments
function previewFile(id) {
    showNotification('فتح معاينة الملف...', 'info');
}

function downloadFile(id) {
    showNotification(`جاري تحميل الملف ${id}...`, 'info');
}

function deleteFile(id) {
    showConfirm('حذف الملف', 'هل تريد حذف هذا الملف؟', 'danger', function() {
        showSuccess('تم حذف الملف');
    });
}

// Chat Functions
function loadConversation(customerId) {
    showNotification(`تحميل محادثة العميل ${customerId}...`, 'info');
}

function attachImage() {
    document.getElementById('imageInput')?.click();
}

function attachFile() {
    document.getElementById('fileInput')?.click();
}

function toggleChatSidebar() {
    const sidebar = document.querySelector('.chat-sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}

function viewRequestDetails(id) {
    window.location.href = `/${id}/`;
}

// Settings & Permissions
function selectAllPermissions() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = true);
}

function clearAllPermissions() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = false);
}

function toggleSelectAll(checkbox) {
    const checkboxes = document.querySelectorAll('.request-checkbox');
    checkboxes.forEach(cb => cb.checked = checkbox.checked);
}

// Smart Alerts
function testAlert(id) {
    showSuccess('تم إرسال تنبيه تجريبي');
}

function deleteAlert(id) {
    showConfirm('حذف التنبيه', 'هل تريد حذف هذا التنبيه؟', 'danger', function() {
        showSuccess('تم حذف التنبيه');
    });
}

// Other Utility Functions
function contactSupport() {
    window.location.href = '/chat/';
}

function contactPrivacy() {
    window.location.href = '/chat/';
}

function contactLegal() {
    window.location.href = '/chat/';
}

function performSearch() {
    const query = document.getElementById('searchQuery')?.value;
    if (query) {
        window.location.href = `/list/?q=${query}`;
    }
}

// ========================================
// Missing Functions (من الفحص)
// ========================================

// Accounts Functions
function forgotPassword() {
    event.preventDefault();
    showNotification('سيتم إضافة صفحة استعادة كلمة المرور قريباً', 'info');
}

function contactAdmin() {
    event.preventDefault();
    window.location.href = '/chat/';
}

function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (passwordInput && toggleIcon) {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        }
    }
}

function changePassword() {
    showNotification('سيتم فتح نموذج تغيير كلمة المرور', 'info');
}

function changeProfilePicture() {
    showNotification('سيتم فتح نافذة اختيار الصورة', 'info');
}

function saveSettings() {
    showSuccess('تم حفظ الإعدادات بنجاح');
}

function saveProfile(event) {
    event.preventDefault();
    showSuccess('تم حفظ البيانات الشخصية بنجاح');
    return false;
}

// Request Functions
function changeStep(step) {
    // التنقل بين خطوات النموذج
    const steps = document.querySelectorAll('.step-content');
    steps.forEach(s => s.classList.remove('active'));
    
    const targetStep = document.getElementById(`step${step}`);
    if (targetStep) {
        targetStep.classList.add('active');
    }
}

function removeImage() {
    const imagePreview = document.getElementById('imagePreview');
    const imageInput = document.getElementById('identityImage');
    
    if (imagePreview) imagePreview.style.display = 'none';
    if (imageInput) imageInput.value = '';
}

function confirmCancel() {
    showConfirm('إلغاء التعديلات', 'هل تريد إلغاء التعديلات والعودة؟', 'warning', function() {
        window.location.href = '/list/';
    });
}

function approveSelected() {
    showConfirm('الموافقة على المحدد', 'هل تريد الموافقة على جميع الطلبات المحددة؟', 'success', function() {
        showSuccess('تمت الموافقة على الطلبات المحددة');
        setTimeout(() => location.reload(), 1500);
    });
}

function rejectSelected() {
    showConfirm('رفض المحدد', 'هل تريد رفض جميع الطلبات المحددة؟', 'danger', function() {
        showWarning('تم رفض الطلبات المحددة');
        setTimeout(() => location.reload(), 1500);
    });
}

function assignRequest(id) {
    showNotification(`تعيين الطلب ${id} لمستخدم`, 'info');
}

function restoreRequest(id) {
    showConfirm('استعادة الطلب', 'هل تريد استعادة هذا الطلب المحذوف؟', 'primary', function() {
        showSuccess('تم استعادة الطلب');
        setTimeout(() => location.reload(), 1500);
    });
}

function exportRequest(id) {
    showNotification(`جاري تصدير الطلب ${id}...`, 'info');
}

function viewDocument(docId) {
    showNotification(`فتح المستند ${docId}...`, 'info');
}

// Template Functions
function clearTemplateFilters() {
    location.reload();
}

function publishTemplate(id) {
    showConfirm('نشر القالب', 'هل تريد نشر هذا القالب؟', 'success', function() {
        showSuccess('تم نشر القالب');
    });
}

// Client Functions
function resolveConflict(id) {
    showNotification(`حل التعارض ${id}`, 'info');
}

function viewResolution(id) {
    showNotification(`عرض تفاصيل الحل ${id}`, 'info');
}

function viewReviewDetails(id) {
    showNotification(`عرض تفاصيل المراجعة ${id}`, 'info');
}

function sendBirthdayGreetings() {
    showConfirm('إرسال التهاني', 'هل تريد إرسال رسائل تهنئة لجميع الأعياد اليوم؟', 'success', function() {
        showSuccess('تم إرسال رسائل التهنئة');
    });
}

function viewCustomerRequests(customerId) {
    window.location.href = `/list/?customer_id=${customerId}`;
}

function addNote() {
    showNotification('إضافة ملاحظة جديدة', 'info');
}

function exportCustomerData(id) {
    showNotification(`جاري تصدير بيانات العميل ${id}...`, 'info');
}

function sendBirthdayGreeting(id) {
    showConfirm('إرسال التهنئة', 'هل تريد إرسال رسالة عيد ميلاد لهذا العميل؟', 'success', function() {
        showSuccess('تم إرسال رسالة التهنئة');
    });
}

// ========================================
// Create Request - Customer Selection
// ========================================

function createNewRequest() {
    window.location.href = '/create/';
}

function toggleCustomerForm() {
    const existingCustomerRadio = document.getElementById('existingCustomer');
    const newCustomerRadio = document.getElementById('newCustomer');
    const existingSection = document.getElementById('existingCustomerSection');
    const newSection = document.getElementById('newCustomerSection');
    
    if (existingCustomerRadio && existingCustomerRadio.checked) {
        // إظهار قسم العميل الموجود وإخفاء قسم العميل الجديد
        if (existingSection) existingSection.classList.remove('d-none');
        if (newSection) newSection.classList.add('d-none');
        
        // إلغاء required من حقول العميل الجديد
        const newCustomerInputs = newSection.querySelectorAll('input[required], select[required]');
        newCustomerInputs.forEach(input => input.removeAttribute('required'));
    } else if (newCustomerRadio && newCustomerRadio.checked) {
        // إظهار قسم العميل الجديد وإخفاء قسم العميل الموجود
        if (newSection) newSection.classList.remove('d-none');
        if (existingSection) existingSection.classList.add('d-none');
        
        // إعادة required لحقول العميل الجديد
        const customerName = document.getElementById('customerName');
        const emiratesId = document.getElementById('emiratesId');
        const dateOfBirth = document.getElementById('dateOfBirth');
        const nationality = document.getElementById('nationality');
        const mobileNumber = document.getElementById('mobileNumber');
        const confirmName = document.getElementById('confirmName');
        
        if (customerName) customerName.setAttribute('required', 'required');
        if (emiratesId) emiratesId.setAttribute('required', 'required');
        if (dateOfBirth) dateOfBirth.setAttribute('required', 'required');
        if (nationality) nationality.setAttribute('required', 'required');
        if (mobileNumber) mobileNumber.setAttribute('required', 'required');
        if (confirmName) confirmName.setAttribute('required', 'required');
    }
}

function selectExistingCustomer(id, name, emiratesId, phone, email) {
    // حفظ ID العميل المختار
    const existingCustomerIdInput = document.getElementById('existingCustomerId');
    if (existingCustomerIdInput) {
        existingCustomerIdInput.value = id;
    }
    
    // إظهار رسالة النجاح
    const selectedAlert = document.getElementById('selectedCustomerAlert');
    const selectedNameSpan = document.getElementById('selectedCustomerName');
    
    if (selectedAlert && selectedNameSpan) {
        selectedNameSpan.textContent = name;
        selectedAlert.classList.remove('d-none');
    }
    
    // إخفاء نتائج البحث
    const searchResults = document.getElementById('customerSearchResults');
    if (searchResults) {
        searchResults.classList.add('d-none');
    }
}

// البحث في العملاء (live search)
function searchCustomers() {
    const searchInput = document.getElementById('customerSearch');
    const searchResults = document.getElementById('customerSearchResults');
    
    if (!searchInput || !searchResults) return;
    
    const searchTerm = searchInput.value.trim();
    
    if (searchTerm.length < 2) {
        // إخفاء النتائج إذا كان البحث أقل من حرفين
        searchResults.innerHTML = `
            <div class="text-center text-muted py-3">
                <i class="fas fa-search fa-2x mb-2 d-block"></i>
                <p>اكتب حرفين على الأقل للبحث</p>
            </div>
        `;
        return;
    }
    
    // هنا يمكن إضافة AJAX call للبحث في قاعدة البيانات
    // حالياً سنعرض رسالة
    searchResults.innerHTML = `
        <div class="text-center text-muted py-3">
            <i class="fas fa-spinner fa-spin fa-2x mb-2 d-block"></i>
            <p>جاري البحث...</p>
        </div>
    `;
}

// Initialize customer search
document.addEventListener('DOMContentLoaded', function() {
    const customerSearchInput = document.getElementById('customerSearch');
    if (customerSearchInput) {
        customerSearchInput.addEventListener('input', searchCustomers);
    }
});
