from django.db import models


class AuditLog(models.Model):
    """سجل شامل لجميع العمليات - لا يُحذف أبداً"""
    
    # نوع العملية
    action = models.CharField('العملية', max_length=50, choices=[
        ('create', 'إنشاء'),
        ('update', 'تعديل'),
        ('delete', 'حذف'),
        ('view', 'عرض'),
        ('approve', 'موافقة'),
        ('reject', 'رفض'),
        ('payment', 'دفع'),
        ('login', 'تسجيل دخول'),
        ('logout', 'تسجيل خروج'),
        ('export', 'تصدير'),
        ('print', 'طباعة'),
        ('restore', 'استعادة'),
    ])
    
    # الكيان المتأثر
    model_name = models.CharField('نوع الكيان', max_length=100)
    object_id = models.IntegerField('معرف الكيان', null=True, blank=True)
    object_repr = models.CharField('تمثيل الكيان', max_length=200)
    
    # المستخدم
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='المستخدم'
    )
    
    # التفاصيل
    description = models.TextField('الوصف')
    old_values = models.JSONField('القيم القديمة', null=True, blank=True)
    new_values = models.JSONField('القيم الجديدة', null=True, blank=True)
    changes = models.JSONField('التغييرات', null=True, blank=True)
    
    # معلومات الجلسة
    ip_address = models.GenericIPAddressField('عنوان IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    session_key = models.CharField('Session Key', max_length=100, blank=True)
    
    # مستوى الأهمية
    severity = models.CharField('الأهمية', max_length=20, choices=[
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية'),
        ('critical', 'حرجة'),
    ], default='medium')
    
    # التاريخ
    timestamp = models.DateTimeField('الوقت', auto_now_add=True)
    
    class Meta:
        verbose_name = 'سجل تدقيق'
        verbose_name_plural = 'سجلات التدقيق'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model_name', 'object_id']),
            models.Index(fields=['user']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.model_name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
