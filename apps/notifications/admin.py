from django.contrib import admin
from .models import Notification, SmartAlert


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """إدارة الإشعارات"""
    
    list_display = ['user', 'title', 'notification_type', 'priority', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    
    fieldsets = (
        ('معلومات الإشعار', {
            'fields': ('user', 'notification_type', 'priority')
        }),
        ('المحتوى', {
            'fields': ('title', 'message', 'action_url')
        }),
        ('الارتباط', {
            'fields': ('request',)
        }),
        ('الحالة', {
            'fields': ('is_read', 'read_at', 'expires_at')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SmartAlert)
class SmartAlertAdmin(admin.ModelAdmin):
    """إدارة التنبيهات الذكية"""
    
    list_display = ['name', 'alert_type', 'frequency', 'is_active', 'execution_count', 'last_run', 'next_run']
    list_filter = ['alert_type', 'frequency', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['last_run', 'next_run', 'execution_count', 'created_at', 'updated_at']
    filter_horizontal = ['target_users']
    
    fieldsets = (
        ('معلومات التنبيه', {
            'fields': ('name', 'description', 'alert_type')
        }),
        ('التوقيت والإجراء', {
            'fields': ('frequency', 'action')
        }),
        ('الشرط', {
            'fields': ('condition',)
        }),
        ('المستهدفون', {
            'fields': ('target_users', 'target_roles')
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
        ('التنفيذ', {
            'fields': ('last_run', 'next_run', 'execution_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
