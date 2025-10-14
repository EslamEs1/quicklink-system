/* Quick Link System - Custom JavaScript */
/* UI & Design Only - No Backend Logic */

// ============================================
// 1. تهيئة النظام عند تحميل الصفحة
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    initializeUI();
    setupSidebarToggle();
    setupAlertAutoDismiss();
    initializeDatePicker();
});

// ============================================
// 2. إعداد تبديل الشريط الجانبي (UI فقط)
// ============================================
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

// ============================================
// 3. تهيئة واجهة المستخدم (UI فقط)
// ============================================
function initializeUI() {
    // تفعيل الروابط النشطة في القائمة
    highlightActiveMenu();
    
    // تهيئة النماذج (UI فقط)
    setupFormUI();
}

// تمييز الرابط النشط في القائمة
function highlightActiveMenu() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/') {
            link.classList.add('active');
        }
    });
}

// إعداد واجهة النماذج
function setupFormUI() {
    // إضافة تأثيرات بصرية للحقول عند التركيز
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement?.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement?.classList.remove('focused');
        });
    });
}

// ============================================
// 4. إدارة التنبيهات (UI فقط)
// ============================================
function setupAlertAutoDismiss() {
    // إخفاء التنبيهات تلقائياً بعد 5 ثوان
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
}

// إظهار تنبيه مخصص (UI فقط)
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; left: 20px; z-index: 9999; min-width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);';
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // إزالة التنبيه تلقائياً بعد 5 ثوان
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.style.opacity = '0';
            alertDiv.style.transition = 'opacity 0.3s ease';
            setTimeout(() => alertDiv.remove(), 300);
        }
    }, 5000);
}

// ============================================
// 5. تهيئة حقول التاريخ (UI فقط)
// ============================================
function initializeDatePicker() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // إضافة تحسينات بصرية للتقويم
        input.addEventListener('change', function() {
            if (this.value) {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            }
        });
    });
}

// ============================================
// 6. وظائف البحث والفلترة (Frontend فقط)
// ============================================
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

function clearFilters() {
    // مسح حقول البحث والفلاتر (UI فقط)
    document.getElementById('searchInput')?.value = '';
    document.getElementById('statusFilter')?.selectedIndex = 0;
    document.getElementById('dateFilter')?.value = '';
    
    // إظهار جميع الصفوف
    const rows = document.querySelectorAll('#requestsTable tbody tr');
    rows.forEach(row => row.style.display = '');
    
    showNotification('تم مسح الفلاتر', 'info');
}

// ============================================
// 7. وظائف الطباعة والتصدير (UI فقط)
// ============================================
function printRequest() {
    window.print();
}

function printRequests() {
    window.print();
}

function exportToExcel() {
    showNotification('جاري تصدير البيانات...', 'info');
    // Django سيتولى التصدير الفعلي
}

// ============================================
// 8. وظائف مساعدة للواجهة
// ============================================

// إخفاء/إظهار كلمة المرور
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.type = input.type === 'password' ? 'text' : 'password';
    }
}

// تأكيد الإجراء (UI فقط)
function confirmAction(message) {
    return confirm(message || 'هل أنت متأكد من هذا الإجراء؟');
}

// تفعيل/تعطيل زر
function toggleButton(buttonId, enable = true) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = !enable;
    }
}

// إضافة تأثير التحميل على الزر
function setButtonLoading(buttonId, loading = true) {
    const button = document.getElementById(buttonId);
    if (button) {
        if (loading) {
            button.disabled = true;
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>جاري التحميل...';
        } else {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText || button.innerHTML;
        }
    }
}

// ============================================
// 9. وظائف WhatsApp والاتصال (فتح في نافذة جديدة فقط)
// ============================================
function callCustomer(customerId) {
    // Django سيتولى إنشاء رابط WhatsApp الصحيح
    // هذه الدالة فقط للتوافق مع الأزرار الموجودة
    console.log('WhatsApp call for customer:', customerId);
}