from django.contrib import admin
from .models import Attachment, Backup


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """إدارة المرفقات"""
    
    list_display = ['file_name', 'request', 'category', 'file_size_mb', 'is_approved', 'uploaded_at']
    list_filter = ['category', 'is_approved', 'file_type', 'uploaded_at']
    search_fields = ['file_name', 'request__reference_number', 'description']
    readonly_fields = ['uploaded_at', 'file_size', 'file_type']
    
    fieldsets = (
        ('الملف', {
            'fields': ('file', 'file_name', 'file_size', 'file_type')
        }),
        ('الارتباط', {
            'fields': ('request', 'category')
        }),
        ('الموافقة', {
            'fields': ('is_approved', 'approved_by', 'approved_at')
        }),
        ('التفاصيل', {
            'fields': ('description', 'notes')
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'uploaded_by'),
            'classes': ('collapse',)
        }),
    )
    
    def file_size_mb(self, obj):
        """عرض الحجم بالميجابايت"""
        return f"{obj.file_size / (1024*1024):.2f} MB"
    file_size_mb.short_description = 'الحجم'


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    """إدارة النسخ الاحتياطية"""
    
    list_display = ['name', 'backup_type', 'status', 'file_size_mb', 'storage_location', 'is_encrypted', 'created_at']
    list_filter = ['backup_type', 'status', 'storage_location', 'is_encrypted', 'created_at']
    search_fields = ['name', 'file_path']
    readonly_fields = ['created_at', 'completed_at']
    
    fieldsets = (
        ('معلومات النسخة', {
            'fields': ('name', 'backup_type', 'status')
        }),
        ('الملف', {
            'fields': ('file_path', 'file_size', 'file_hash')
        }),
        ('التشفير', {
            'fields': ('is_encrypted', 'encryption_method')
        }),
        ('التخزين', {
            'fields': ('storage_location',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'completed_at', 'expires_at')
        }),
        ('Metadata', {
            'fields': ('created_by', 'notes', 'error_message'),
            'classes': ('collapse',)
        }),
    )
    
    def file_size_mb(self, obj):
        """عرض الحجم بالميجابايت"""
        return f"{obj.file_size / (1024*1024):.2f} MB"
    file_size_mb.short_description = 'الحجم'
