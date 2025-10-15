from django.contrib import admin
from django.contrib import messages
from .models import Customer, IdentityConflict


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """إدارة العملاء"""
    
    list_display = ['full_name', 'masked_emirates_id', 'masked_phone', 'age', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_verified', 'gender', 'nationality', 'created_at']
    search_fields = ['full_name', 'full_name_english', 'emirates_id', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at', 'masked_emirates_id', 'masked_phone', 'age']
    actions = ['delete_selected_customers', 'deactivate_customers']
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('full_name', 'full_name_english', 'emirates_id', 'masked_emirates_id')
        }),
        ('المعلومات الشخصية', {
            'fields': ('date_of_birth', 'age', 'nationality', 'gender')
        }),
        ('معلومات الاتصال', {
            'fields': ('phone', 'masked_phone', 'email', 'address')
        }),
        ('معلومات إضافية', {
            'fields': ('occupation', 'company_name', 'notes')
        }),
        ('الحالة', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    def delete_selected_customers(self, request, queryset):
        """حذف العملاء المحددين نهائياً"""
        deleted_count = 0
        skipped_count = 0
        
        for customer in queryset:
            # التحقق من وجود طلبات مرتبطة
            if customer.requests.count() > 0:
                skipped_count += 1
                continue
            
            # حذف العميل نهائياً
            customer_name = customer.full_name
            customer.delete()
            deleted_count += 1
        
        if deleted_count > 0:
            messages.success(request, f'تم حذف {deleted_count} عميل نهائياً من النظام')
        
        if skipped_count > 0:
            messages.warning(request, f'تم تخطي {skipped_count} عميل بسبب وجود طلبات مرتبطة')
    
    delete_selected_customers.short_description = "حذف العملاء المحددين نهائياً"
    
    def deactivate_customers(self, request, queryset):
        """تعطيل العملاء المحددين (soft delete)"""
        updated_count = queryset.update(is_active=False)
        messages.success(request, f'تم تعطيل {updated_count} عميل')
    
    deactivate_customers.short_description = "تعطيل العملاء المحددين"


@admin.register(IdentityConflict)
class IdentityConflictAdmin(admin.ModelAdmin):
    """إدارة تعارضات الهوية"""
    
    list_display = ['customer1', 'customer2', 'conflict_type', 'status', 'detected_at']
    list_filter = ['conflict_type', 'status', 'detected_at']
    search_fields = ['customer1__full_name', 'customer2__full_name']
    readonly_fields = ['detected_at']
    
    fieldsets = (
        ('التعارض', {
            'fields': ('customer1', 'customer2', 'conflict_type')
        }),
        ('الحالة والحل', {
            'fields': ('status', 'resolution', 'resolved_by', 'resolved_at')
        }),
        ('Metadata', {
            'fields': ('detected_at',)
        }),
    )
