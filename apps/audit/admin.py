from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """إدارة سجل التدقيق - للعرض فقط"""
    
    list_display = ['user', 'action', 'model_name', 'object_repr', 'severity', 'timestamp']
    list_filter = ['action', 'model_name', 'severity', 'timestamp']
    search_fields = ['user__username', 'model_name', 'object_repr', 'description']
    readonly_fields = ['action', 'model_name', 'object_id', 'object_repr', 'user', 'description', 
                       'old_values', 'new_values', 'changes', 'ip_address', 'user_agent', 
                       'session_key', 'severity', 'timestamp']
    
    # منع الحذف والتعديل - للعرض فقط
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        ('معلومات العملية', {
            'fields': ('action', 'model_name', 'object_id', 'object_repr', 'severity')
        }),
        ('المستخدم', {
            'fields': ('user', 'ip_address', 'user_agent', 'session_key')
        }),
        ('التفاصيل', {
            'fields': ('description', 'old_values', 'new_values', 'changes')
        }),
        ('التوقيت', {
            'fields': ('timestamp',)
        }),
    )
