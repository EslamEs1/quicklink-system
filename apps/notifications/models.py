from django.db import models


class Notification(models.Model):
    """الإشعارات والتنبيهات"""
    
    # المستخدم المستهدف
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='المستخدم'
    )
    
    # نوع الإشعار
    notification_type = models.CharField('النوع', max_length=50, choices=[
        ('request_new', 'طلب جديد'),
        ('request_approved', 'طلب موافق عليه'),
        ('request_rejected', 'طلب مرفوض'),
        ('payment_pending', 'دفع معلق'),
        ('payment_completed', 'دفع مكتمل'),
        ('birthday', 'عيد ميلاد'),
        ('identity_conflict', 'تعارض هوية'),
        ('overdue', 'طلب متأخر'),
        ('system', 'نظام'),
    ])
    
    # المحتوى
    title = models.CharField('العنوان', max_length=200)
    message = models.TextField('الرسالة')
    
    # الأولوية
    priority = models.CharField('الأولوية', max_length=20, choices=[
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية'),
        ('critical', 'حرجة'),
    ], default='medium')
    
    # الحالة
    is_read = models.BooleanField('مقروء', default=False)
    read_at = models.DateTimeField('تاريخ القراءة', null=True, blank=True)
    
    # الارتباط (اختياري)
    request = models.ForeignKey(
        'requests.Request',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    # Action URL
    action_url = models.CharField('رابط الإجراء', max_length=500, blank=True)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    expires_at = models.DateTimeField('تاريخ الانتهاء', null=True, blank=True)
    
    class Meta:
        verbose_name = 'إشعار'
        verbose_name_plural = 'الإشعارات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        """وضع علامة مقروء"""
        from datetime import datetime
        self.is_read = True
        self.read_at = datetime.now()
        self.save()


class SmartAlert(models.Model):
    """التنبيهات الذكية التلقائية"""
    
    # معلومات التنبيه
    name = models.CharField('اسم التنبيه', max_length=200)
    description = models.TextField('الوصف')
    
    # نوع التنبيه
    alert_type = models.CharField('النوع', max_length=50, choices=[
        ('overdue_requests', 'طلبات متأخرة'),
        ('birthday', 'أعياد ميلاد'),
        ('identity_conflict', 'تعارضات الهوية'),
        ('backup', 'النسخ الاحتياطي'),
        ('pending_payment', 'مدفوعات معلقة'),
        ('missing_docs', 'مستندات ناقصة'),
        ('approval_needed', 'تحتاج موافقة'),
        ('custom', 'مخصص'),
    ])
    
    # الشرط
    condition = models.TextField('الشرط')  # JSON أو expression
    
    # التوقيت
    frequency = models.CharField('التكرار', max_length=20, choices=[
        ('realtime', 'فوري'),
        ('hourly', 'كل ساعة'),
        ('daily', 'يومياً'),
        ('weekly', 'أسبوعياً'),
        ('monthly', 'شهرياً'),
    ], default='daily')
    
    # الإجراء
    action = models.CharField('الإجراء', max_length=100, choices=[
        ('notify_user', 'إشعار المستخدم'),
        ('send_email', 'إرسال بريد'),
        ('send_sms', 'إرسال رسالة'),
        ('all', 'جميع ما سبق'),
    ], default='notify_user')
    
    # المستهدفون
    target_users = models.ManyToManyField('auth.User', blank=True, verbose_name='المستخدمون المستهدفون')
    target_roles = models.JSONField('الأدوار المستهدفة', default=list)
    
    # الحالة
    is_active = models.BooleanField('نشط', default=True)
    
    # آخر تنفيذ
    last_run = models.DateTimeField('آخر تنفيذ', null=True, blank=True)
    next_run = models.DateTimeField('التنفيذ القادم', null=True, blank=True)
    execution_count = models.IntegerField('عدد مرات التنفيذ', default=0)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='alerts_created')
    
    class Meta:
        verbose_name = 'تنبيه ذكي'
        verbose_name_plural = 'التنبيهات الذكية'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"
