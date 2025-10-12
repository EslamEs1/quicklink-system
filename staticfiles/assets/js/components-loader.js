/* Quick Link System - Components Loader */

// تحميل المكونات بشكل صحيح بدون مشاكل
(function() {
    'use strict';
    
    // تحميل المكونات عند جاهزية الصفحة
    document.addEventListener('DOMContentLoaded', async function() {
        try {
            // تحميل جميع المكونات
            const [header, sidebar, footer, modal] = await Promise.all([
                fetch('components/header.html').then(r => r.ok ? r.text() : ''),
                fetch('components/sidebar.html').then(r => r.ok ? r.text() : ''),
                fetch('components/footer.html').then(r => r.ok ? r.text() : ''),
                fetch('components/confirm-modal.html').then(r => r.ok ? r.text() : '')
            ]);
            
            // إدراج المكونات في الصفحة
            const headerEl = document.getElementById('header-placeholder');
            const sidebarEl = document.getElementById('sidebar-placeholder');
            const footerEl = document.getElementById('footer-placeholder');
            const modalEl = document.getElementById('modal-placeholder');
            
            if (headerEl && header) headerEl.innerHTML = header;
            if (sidebarEl && sidebar) sidebarEl.innerHTML = sidebar;
            if (footerEl && footer) footerEl.innerHTML = footer;
            if (modalEl && modal) modalEl.innerHTML = modal;
            
            // الانتظار لحظة لضمان إدراج المكونات في DOM
            await new Promise(resolve => setTimeout(resolve, 50));
            
            // تهيئة النظام بعد تحميل المكونات
            if (typeof initializeSystem === 'function') {
                initializeSystem();
            }
            
            if (typeof setupSidebarToggle === 'function') {
                setupSidebarToggle();
            }
            
        } catch (error) {
            console.error('خطأ في تحميل المكونات:', error);
        }
    });
})();

