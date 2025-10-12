from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """إدارة ملفات المستخدمين"""
    
    list_display = ['user', 'employee_id', 'role', 'department', 'job_title', 'is_active']
    list_filter = ['role', 'department', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'last_activity']
    
    fieldsets = (
        ('المستخدم', {
            'fields': ('user', 'employee_id')
        }),
        ('المعلومات الوظيفية', {
            'fields': ('role', 'department', 'job_title', 'phone')
        }),
        ('الصورة', {
            'fields': ('avatar',)
        }),
        ('الإعدادات', {
            'fields': ('receive_email_notifications', 'receive_sms_notifications', 'language')
        }),
        ('الإحصائيات', {
            'fields': ('requests_handled', 'customers_managed'),
            'classes': ('collapse',)
        }),
        ('النشاط', {
            'fields': ('last_login_ip', 'last_activity'),
            'classes': ('collapse',)
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
