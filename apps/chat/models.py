from django.db import models


class ChatMessage(models.Model):
    """رسائل WhatsApp Business - آمنة ومخفية"""
    
    # المحادثة
    customer = models.ForeignKey(
        'clients.Customer',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='العميل'
    )
    
    request = models.ForeignKey(
        'requests.Request',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        verbose_name='الطلب المرتبط'
    )
    
    # الرسالة
    message_type = models.CharField('النوع', max_length=20, choices=[
        ('text', 'نص'),
        ('image', 'صورة'),
        ('document', 'مستند'),
        ('video', 'فيديو'),
        ('audio', 'صوت'),
    ], default='text')
    
    content = models.TextField('المحتوى')
    file = models.FileField('ملف مرفق', upload_to='chat/%Y/%m/', blank=True)
    
    # الاتجاه
    direction = models.CharField('الاتجاه', max_length=10, choices=[
        ('incoming', 'وارد'),
        ('outgoing', 'صادر'),
    ])
    
    # المرسل/المستقبل
    sent_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='المرسل',
        blank=True
    )
    
    # الحالة
    is_read = models.BooleanField('مقروء', default=False)
    read_at = models.DateTimeField('تاريخ القراءة', null=True, blank=True)
    
    delivery_status = models.CharField('حالة التوصيل', max_length=20, choices=[
        ('pending', 'معلق'),
        ('sent', 'مرسل'),
        ('delivered', 'تم التوصيل'),
        ('read', 'مقروء'),
        ('failed', 'فشل'),
    ], default='pending')
    
    # WhatsApp API Info
    whatsapp_message_id = models.CharField('WhatsApp Message ID', max_length=100, blank=True, unique=True, null=True)
    
    # Metadata
    sent_at = models.DateTimeField('تاريخ الإرسال', auto_now_add=True)
    delivered_at = models.DateTimeField('تاريخ التوصيل', null=True, blank=True)
    
    class Meta:
        verbose_name = 'رسالة'
        verbose_name_plural = 'الرسائل'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['customer', 'sent_at']),
            models.Index(fields=['whatsapp_message_id']),
        ]
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.get_direction_display()} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
