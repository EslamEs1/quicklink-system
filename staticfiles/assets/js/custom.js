/* Quick Link System - Custom JavaScript */
/* UI & Design Only - No Backend Logic */

// ============================================
// 1. تهيئة النظام عند تحميل الصفحة
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    setupSidebarToggle();
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

