from django.contrib import admin
from .models import SystemSetting


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    """إدارة إعدادات النظام"""
    
    list_display = ['key', 'value_preview', 'category', 'setting_type', 'is_active']
    list_filter = ['category', 'setting_type', 'is_active']
    search_fields = ['key', 'value', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('الإعداد', {
            'fields': ('key', 'value', 'setting_type', 'category')
        }),
        ('الوصف', {
            'fields': ('description',)
        }),
        ('الحالة', {
            'fields': ('is_active', 'is_editable')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    def value_preview(self, obj):
        """معاينة القيمة (50 حرف)"""
        return obj.value[:50] + '...' if len(obj.value) > 50 else obj.value
    value_preview.short_description = 'القيمة'
