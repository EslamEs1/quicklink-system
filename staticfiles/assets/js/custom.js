/* Quick Link System - Custom JavaScript */

// تهيئة النظام عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // تحميل سريع للعناصر الأساسية أولاً
    initializeSystem();
    setupSidebarToggle();
});

// إعداد تبديل الشريط الجانبي
function setupSidebarToggle() {
    // إخفاء الشريط الجانبي على الشاشات الصغيرة
    if (window.innerWidth <= 768) {
        document.querySelector('.sidebar')?.classList.remove('show');
    }
    
    // إضافة مستمع لحجم الشاشة
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            document.querySelector('.sidebar')?.classList.add('show');
        } else {
            document.querySelector('.sidebar')?.classList.remove('show');
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

// وظائف التهيئة
function initializeSystem() {
    // تهيئة النماذج
    initializeForms();
    
    // تهيئة التنبيهات
    initializeNotifications();
    
    // تهيئة الجداول
    initializeTables();
    
    // تهيئة القوائم
    initializeSidebar();
    
    // تهيئة التحقق من صحة البيانات
    initializeValidation();
    
    // تهيئة الأرقام المرجعية
    initializeReferenceNumbers();
}

// تهيئة النماذج
function initializeForms() {
    // لا توجد تأثيرات مطلوبة
}

// تهيئة التنبيهات
function initializeNotifications() {
    // إخفاء التنبيهات تلقائياً بعد 5 ثوان
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
}

// تهيئة الجداول
function initializeTables() {
    // لا توجد تأثيرات مطلوبة
}

// تهيئة الشريط الجانبي
function initializeSidebar() {
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // إزالة الفئة النشطة من جميع الروابط
            navLinks.forEach(l => l.classList.remove('active'));
            
            // إضافة الفئة النشطة للرابط المحدد
            this.classList.add('active');
        });
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

// وظائف إدارة الطلبات
function createNewRequest() {
    window.location.href = '/requests/create/';
}

// عرض الطلب
function viewRequest(id) {
    window.location.href = `/requests/${id}/`;
}

// تعديل الطلب
function editRequest(id) {
    window.location.href = `/requests/${id}/edit/`;
}

// حذف الطلب
function deleteRequest(id, referenceNumber) {
    if (confirm(`هل أنت متأكد من حذف الطلب ${referenceNumber}؟\n\nهذا الإجراء لا يمكن التراجع عنه!`)) {
        // إنشاء form وإرساله
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/requests/${id}/delete/`;
        
        // إضافة CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken.value;
            form.appendChild(csrfInput);
        }
        
        document.body.appendChild(form);
        form.submit();
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
function processPayment(requestId) {
    window.location.href = `/payments/?request_id=${requestId}`;
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
        // إضافة تحسينات للتقويم
        input.addEventListener('change', function() {
            if (this.value) {
                this.classList.add('is-valid');
            }
        });
    });
}

// وظائف الطباعة
function printRequest(requestId) {
    window.print();
}

// تصدير البيانات
function exportToExcel() {
    showNotification('جاري تصدير البيانات...', 'info');
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

// تهيئة النظام عند تحميل الصفحة
window.addEventListener('load', function() {
    // تهيئة التقويم
    initializeDatePicker();
});