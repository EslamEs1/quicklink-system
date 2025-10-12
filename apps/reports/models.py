from django.db import models


class Report(models.Model):
    """التقارير المحفوظة"""
    
    # معلومات التقرير
    name = models.CharField('اسم التقرير', max_length=200)
    description = models.TextField('الوصف', blank=True)
    
    # النوع
    report_type = models.CharField('نوع التقرير', max_length=100, choices=[
        ('requests_summary', 'ملخص الطلبات'),
        ('customers_summary', 'ملخص العملاء'),
        ('payments_summary', 'ملخص المدفوعات'),
        ('audit_trail', 'سجل التدقيق'),
        ('performance', 'الأداء'),
        ('custom', 'مخصص'),
    ])
    
    # الفترة الزمنية
    start_date = models.DateField('من تاريخ', null=True, blank=True)
    end_date = models.DateField('إلى تاريخ', null=True, blank=True)
    
    # الفلاتر
    filters = models.JSONField('الفلاتر', default=dict)
    
    # النتائج
    results = models.JSONField('النتائج', null=True, blank=True)
    
    # الملف المولّد
    file = models.FileField('ملف التقرير', upload_to='reports/%Y/%m/', blank=True)
    file_format = models.CharField('صيغة الملف', max_length=20, choices=[
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ], default='pdf')
    
    # الحالة
    status = models.CharField('الحالة', max_length=20, choices=[
        ('pending', 'معلق'),
        ('generating', 'جارٍ التوليد'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
    ], default='pending')
    
    # Metadata
    generated_at = models.DateTimeField('تاريخ التوليد', auto_now_add=True)
    generated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='تم التوليد بواسطة'
    )
    
    # آخر تحميل
    last_downloaded_at = models.DateTimeField('آخر تحميل', null=True, blank=True)
    download_count = models.IntegerField('عدد التحميلات', default=0)
    
    class Meta:
        verbose_name = 'تقرير'
        verbose_name_plural = 'التقارير'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.name} - {self.generated_at.strftime('%Y-%m-%d')}"
