from django.db import models
from django.core.validators import RegexValidator
from datetime import date


class Customer(models.Model):
    """ملف العميل المركزي الدائم"""
    
    # معلومات أساسية
    full_name = models.CharField('الاسم الرباعي', max_length=200)
    full_name_english = models.CharField('الاسم بالإنجليزية', max_length=200, blank=True)
    
    # رقم الهوية الإماراتية (784-XXXX-XXXXXXX-X)
    emirates_id = models.CharField(
        'رقم الهوية',
        max_length=18,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^784-\d{4}-\d{7}-\d{1}$',
                message='رقم الهوية يجب أن يكون بصيغة: 784-XXXX-XXXXXXX-X'
            )
        ]
    )
    
    # معلومات شخصية
    date_of_birth = models.DateField('تاريخ الميلاد')
    nationality = models.CharField('الجنسية', max_length=100, default='الإمارات')
    gender = models.CharField('الجنس', max_length=10, choices=[
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    ])
    
    # معلومات الاتصال (مخفية)
    phone = models.CharField('رقم الجوال', max_length=20)
    email = models.EmailField('البريد الإلكتروني', blank=True)
    address = models.TextField('العنوان', blank=True)
    
    # صورة الهوية (تحفظ مع العميل)
    id_image = models.ImageField('صورة الهوية الإماراتية', upload_to='customer_ids/', blank=True, null=True)
    
    # معلومات إضافية
    occupation = models.CharField('المهنة', max_length=100, blank=True)
    company_name = models.CharField('اسم الشركة', max_length=200, blank=True)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='customers_created',
        verbose_name='تم الإنشاء بواسطة'
    )
    
    # Status
    is_active = models.BooleanField('نشط', default=True)
    is_verified = models.BooleanField('موثق', default=False)
    
    # Notes
    notes = models.TextField('ملاحظات', blank=True)
    
    class Meta:
        verbose_name = 'عميل'
        verbose_name_plural = 'العملاء'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['emirates_id']),
            models.Index(fields=['full_name']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.masked_emirates_id}"
    
    @property
    def masked_emirates_id(self):
        """رقم الهوية المخفي جزئياً"""
        return f"{self.emirates_id[:3]}-****-{self.emirates_id[-9:-2]}-{self.emirates_id[-1]}"
    
    @property
    def masked_phone(self):
        """رقم الجوال المخفي"""
        if len(self.phone) >= 10:
            return f"{self.phone[:3]}-****-{self.phone[-3:]}"
        return "****"
    
    @property
    def age(self):
        """حساب العمر"""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def is_birthday_today(self):
        """هل اليوم عيد ميلاده؟"""
        today = date.today()
        return (today.month, today.day) == (self.date_of_birth.month, self.date_of_birth.day)


class IdentityConflict(models.Model):
    """كشف تعارضات الهوية"""
    
    # العملاء المتعارضون
    customer1 = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='conflicts_as_first',
        verbose_name='العميل الأول'
    )
    
    customer2 = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='conflicts_as_second',
        verbose_name='العميل الثاني'
    )
    
    # نوع التعارض
    conflict_type = models.CharField('نوع التعارض', max_length=50, choices=[
        ('same_name_diff_id', 'نفس الاسم - هوية مختلفة'),
        ('same_id_diff_name', 'نفس الهوية - اسم مختلف'),
        ('similar_name', 'أسماء متشابهة'),
    ])
    
    # الحالة
    status = models.CharField('الحالة', max_length=20, choices=[
        ('pending', 'معلق'),
        ('reviewing', 'قيد المراجعة'),
        ('resolved', 'تم الحل'),
        ('ignored', 'تم التجاهل'),
    ], default='pending')
    
    # الحل
    resolution = models.TextField('الحل', blank=True)
    resolved_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='تم الحل بواسطة'
    )
    resolved_at = models.DateTimeField('تاريخ الحل', null=True, blank=True)
    
    # Metadata
    detected_at = models.DateTimeField('تاريخ الاكتشاف', auto_now_add=True)
    
    class Meta:
        verbose_name = 'تعارض هوية'
        verbose_name_plural = 'تعارضات الهوية'
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.get_conflict_type_display()} - {self.customer1.full_name}"
