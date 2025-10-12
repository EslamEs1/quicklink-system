from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """إدارة التقارير"""
    
    list_display = ['name', 'report_type', 'status', 'start_date', 'end_date', 'download_count', 'generated_at']
    list_filter = ['report_type', 'status', 'file_format', 'generated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['generated_at', 'last_downloaded_at', 'download_count']
    
    fieldsets = (
        ('معلومات التقرير', {
            'fields': ('name', 'description', 'report_type')
        }),
        ('الفترة الزمنية', {
            'fields': ('start_date', 'end_date')
        }),
        ('الفلاتر', {
            'fields': ('filters',)
        }),
        ('النتائج', {
            'fields': ('results',),
            'classes': ('collapse',)
        }),
        ('الملف', {
            'fields': ('file', 'file_format')
        }),
        ('الحالة', {
            'fields': ('status',)
        }),
        ('الإحصائيات', {
            'fields': ('download_count', 'last_downloaded_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('generated_at', 'generated_by'),
            'classes': ('collapse',)
        }),
    )
