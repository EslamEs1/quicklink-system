from django.db import models


class SystemSetting(models.Model):
    """إعدادات النظام العامة"""
    
    # المفتاح والقيمة
    key = models.CharField('المفتاح', max_length=100, unique=True)
    value = models.TextField('القيمة')
    
    # النوع
    setting_type = models.CharField('النوع', max_length=20, choices=[
        ('string', 'نص'),
        ('number', 'رقم'),
        ('boolean', 'صح/خطأ'),
        ('json', 'JSON'),
    ], default='string')
    
    # التصنيف
    category = models.CharField('التصنيف', max_length=100, choices=[
        ('general', 'عام'),
        ('payment', 'الدفع'),
        ('notifications', 'الإشعارات'),
        ('security', 'الأمان'),
        ('backup', 'النسخ الاحتياطي'),
        ('email', 'البريد الإلكتروني'),
        ('sms', 'الرسائل'),
    ])
    
    # الوصف
    description = models.TextField('الوصف', blank=True)
    
    # الحالة
    is_active = models.BooleanField('نشط', default=True)
    is_editable = models.BooleanField('قابل للتعديل', default=True)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    updated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='تم التحديث بواسطة'
    )
    
    class Meta:
        verbose_name = 'إعداد نظام'
        verbose_name_plural = 'إعدادات النظام'
        ordering = ['category', 'key']
    
    def __str__(self):
        return f"{self.key} = {self.value[:50]}"
