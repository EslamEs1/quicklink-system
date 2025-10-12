from django.db import models


class Payment(models.Model):
    """معلومات الدفع"""
    
    # الطلب المرتبط
    request = models.OneToOneField(
        'requests.Request',
        on_delete=models.PROTECT,
        related_name='payment',
        verbose_name='الطلب'
    )
    
    # معلومات الدفع
    amount = models.DecimalField('المبلغ', max_digits=10, decimal_places=2)
    currency = models.CharField('العملة', max_length=3, default='AED')
    
    # الحالة
    status = models.CharField('حالة الدفع', max_length=20, choices=[
        ('pending', 'معلق'),
        ('processing', 'قيد المعالجة'),
        ('paid', 'مدفوع'),
        ('failed', 'فشل'),
        ('refunded', 'مسترد'),
        ('cancelled', 'ملغي'),
    ], default='pending')
    
    # PayTabs Info
    payment_method = models.CharField('طريقة الدفع', max_length=50, choices=[
        ('paytabs', 'PayTabs'),
        ('cash', 'نقدي'),
        ('bank_transfer', 'تحويل بنكي'),
    ], default='paytabs')
    
    transaction_id = models.CharField('رقم المعاملة', max_length=100, blank=True, unique=True, null=True)
    payment_url = models.URLField('رابط الدفع', blank=True)
    
    # البوابة
    gateway_response = models.JSONField('استجابة البوابة', null=True, blank=True)
    
    # التواريخ
    payment_date = models.DateTimeField('تاريخ الدفع', null=True, blank=True)
    expiry_date = models.DateTimeField('تاريخ انتهاء الرابط', null=True, blank=True)
    
    # معلومات إضافية
    payment_reference = models.CharField('المرجع', max_length=100, blank=True)
    receipt_number = models.CharField('رقم الإيصال', max_length=100, blank=True)
    notes = models.TextField('ملاحظات', blank=True)
    
    # الاسترداد
    refund_amount = models.DecimalField('مبلغ الاسترداد', max_digits=10, decimal_places=2, default=0)
    refund_reason = models.TextField('سبب الاسترداد', blank=True)
    refunded_at = models.DateTimeField('تاريخ الاسترداد', null=True, blank=True)
    refunded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='refunds_processed',
        verbose_name='تم الاسترداد بواسطة'
    )
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    processed_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='تمت المعالجة بواسطة'
    )
    
    class Meta:
        verbose_name = 'دفعة'
        verbose_name_plural = 'المدفوعات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Payment for {self.request.reference_number} - {self.amount} {self.currency}"
    
    @property
    def is_paid(self):
        return self.status == 'paid'
    
    @property
    def is_refunded(self):
        return self.status == 'refunded'
    
    @property
    def is_expired(self):
        """هل انتهت صلاحية رابط الدفع؟"""
        if self.expiry_date:
            from datetime import datetime
            return datetime.now() > self.expiry_date
        return False
