from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """إدارة المدفوعات"""
    
    list_display = ['request', 'amount', 'currency', 'status', 'payment_method', 'transaction_id', 'payment_date']
    list_filter = ['status', 'payment_method', 'payment_date', 'created_at']
    search_fields = ['request__reference_number', 'transaction_id', 'receipt_number']
    readonly_fields = ['created_at', 'updated_at', 'is_paid', 'is_refunded', 'is_expired']
    
    fieldsets = (
        ('معلومات الدفع', {
            'fields': ('request', 'amount', 'currency', 'payment_method')
        }),
        ('الحالة', {
            'fields': ('status', 'is_paid', 'is_refunded', 'is_expired')
        }),
        ('PayTabs', {
            'fields': ('transaction_id', 'payment_url', 'payment_reference', 'receipt_number', 'gateway_response')
        }),
        ('التواريخ', {
            'fields': ('payment_date', 'expiry_date')
        }),
        ('الاسترداد', {
            'fields': ('refund_amount', 'refund_reason', 'refunded_at', 'refunded_by'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('notes', 'processed_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
