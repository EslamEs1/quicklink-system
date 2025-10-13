from django.contrib import admin
from .models import Request, Template, RequestType, RequestCategory


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """إدارة الطلبات"""
    
    list_display = ['reference_number', 'customer', 'status', 'priority', 'is_paid', 'days_pending', 'created_at']
    list_filter = ['status', 'priority', 'is_paid', 'request_type', 'created_at']
    search_fields = ['reference_number', 'customer__full_name', 'description']
    readonly_fields = ['reference_number', 'created_at', 'updated_at', 'days_pending', 'is_overdue']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('reference_number', 'customer', 'request_type', 'template')
        }),
        ('الحالة', {
            'fields': ('status', 'priority', 'is_overdue', 'days_pending')
        }),
        ('الموافقة/الرفض', {
            'fields': ('needs_approval', 'approved_by', 'approved_at', 'rejected_by', 'rejected_at', 'rejection_reason')
        }),
        ('التواريخ', {
            'fields': ('submission_date', 'due_date', 'completion_date')
        }),
        ('الدفع', {
            'fields': ('total_amount', 'is_paid', 'payment_method')
        }),
        ('البيانات الإضافية', {
            'fields': ('description', 'notes', 'internal_notes')
        }),
        ('Checklist', {
            'fields': ('checklist_completed', 'identity_verified', 'template_selected', 'payment_confirmed')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by', 'assigned_to'),
            'classes': ('collapse',)
        }),
        ('Soft Delete', {
            'fields': ('is_deleted', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # لا نعرض المحذوفات في Admin
        return qs.filter(is_deleted=False)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """إدارة القوالب القانونية"""
    
    list_display = ['name', 'code', 'template_type', 'version', 'is_active', 'is_published', 'usage_count']
    list_filter = ['template_type', 'is_active', 'is_published', 'created_at']
    search_fields = ['name', 'name_english', 'code']
    readonly_fields = ['usage_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name', 'name_english', 'code', 'template_type', 'version')
        }),
        ('المحتوى', {
            'fields': ('content_arabic', 'content_english', 'file')
        }),
        ('الحالة والصلاحيات', {
            'fields': ('is_active', 'is_published', 'requires_admin_approval')
        }),
        ('الإحصائيات', {
            'fields': ('usage_count',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RequestCategory)
class RequestCategoryAdmin(admin.ModelAdmin):
    """إدارة فئات الطلبات"""
    
    list_display = ['name_arabic', 'code', 'icon', 'color', 'display_order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_arabic', 'name_english', 'code']
    readonly_fields = ['code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name_arabic', 'name_english', 'code')
        }),
        ('المظهر', {
            'fields': ('icon', 'color', 'display_order')
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RequestType)
class RequestTypeAdmin(admin.ModelAdmin):
    """إدارة أنواع الطلبات"""
    
    list_display = ['name_arabic', 'code', 'category', 'default_price', 'usage_count', 'display_order', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name_arabic', 'name_english', 'code']
    readonly_fields = ['code', 'usage_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name_arabic', 'name_english', 'code', 'category')
        }),
        ('التفاصيل', {
            'fields': ('description', 'default_price', 'display_order')
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
        ('الإحصائيات', {
            'fields': ('usage_count',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
