from django.db import models


class Attachment(models.Model):
    """المرفقات والملفات"""
    
    # الارتباط
    request = models.ForeignKey(
        'requests.Request',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='الطلب'
    )
    
    # الملف
    file = models.FileField('الملف', upload_to='attachments/%Y/%m/')
    file_name = models.CharField('اسم الملف', max_length=255)
    file_size = models.IntegerField('حجم الملف (بايت)')
    file_type = models.CharField('نوع الملف', max_length=50)
    
    # التصنيف
    category = models.CharField('التصنيف', max_length=100, choices=[
        ('identity', 'صورة الهوية'),
        ('authorization', 'التفويض'),
        ('contract', 'عقد'),
        ('receipt', 'إيصال'),
        ('other', 'أخرى'),
    ])
    
    # الحالة
    is_approved = models.BooleanField('موافق عليه', default=False)
    approved_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attachments_approved'
    )
    approved_at = models.DateTimeField('تاريخ الموافقة', null=True, blank=True)
    
    # الملاحظات
    description = models.TextField('الوصف', blank=True)
    notes = models.TextField('ملاحظات', blank=True)
    
    # Metadata
    uploaded_at = models.DateTimeField('تاريخ الرفع', auto_now_add=True)
    uploaded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='تم الرفع بواسطة'
    )
    
    class Meta:
        verbose_name = 'مرفق'
        verbose_name_plural = 'المرفقات'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.file_name} - {self.request.reference_number}"


class Backup(models.Model):
    """سجل النسخ الاحتياطي"""
    
    # معلومات النسخة
    name = models.CharField('اسم النسخة', max_length=200)
    file_path = models.CharField('مسار الملف', max_length=500)
    file_size = models.BigIntegerField('حجم الملف (بايت)')
    
    # النوع
    backup_type = models.CharField('النوع', max_length=20, choices=[
        ('automatic', 'تلقائي'),
        ('manual', 'يدوي'),
        ('scheduled', 'مجدول'),
    ])
    
    # الحالة
    status = models.CharField('الحالة', max_length=20, choices=[
        ('in_progress', 'جارٍ'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
        ('verified', 'تم التحقق'),
    ], default='in_progress')
    
    # التشفير
    is_encrypted = models.BooleanField('مشفر', default=True)
    encryption_method = models.CharField('طريقة التشفير', max_length=50, default='AES-256')
    
    # التخزين
    storage_location = models.CharField('موقع التخزين', max_length=100, choices=[
        ('aws_s3', 'AWS S3'),
        ('google_drive', 'Google Drive'),
        ('local', 'محلي'),
    ])
    
    # hash للتحقق
    file_hash = models.CharField('Hash', max_length=128, blank=True)
    
    # التواريخ
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    completed_at = models.DateTimeField('تاريخ الإكمال', null=True, blank=True)
    expires_at = models.DateTimeField('تاريخ الانتهاء', null=True, blank=True)
    
    # من أنشأ
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='تم الإنشاء بواسطة'
    )
    
    # ملاحظات
    notes = models.TextField('ملاحظات', blank=True)
    error_message = models.TextField('رسالة الخطأ', blank=True)
    
    class Meta:
        verbose_name = 'نسخة احتياطية'
        verbose_name_plural = 'النسخ الاحتياطية'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
