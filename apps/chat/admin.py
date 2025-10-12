from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """إدارة رسائل WhatsApp"""
    
    list_display = ['customer', 'direction', 'message_type', 'delivery_status', 'is_read', 'sent_at']
    list_filter = ['direction', 'message_type', 'delivery_status', 'is_read', 'sent_at']
    search_fields = ['customer__full_name', 'content', 'whatsapp_message_id']
    readonly_fields = ['sent_at', 'delivered_at', 'read_at']
    
    fieldsets = (
        ('المحادثة', {
            'fields': ('customer', 'request', 'direction')
        }),
        ('الرسالة', {
            'fields': ('message_type', 'content', 'file')
        }),
        ('المرسل', {
            'fields': ('sent_by',)
        }),
        ('الحالة', {
            'fields': ('delivery_status', 'is_read', 'read_at')
        }),
        ('WhatsApp Info', {
            'fields': ('whatsapp_message_id',),
            'classes': ('collapse',)
        }),
        ('التواريخ', {
            'fields': ('sent_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
