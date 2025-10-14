from django.db import models
from datetime import datetime, date


class RequestStatus(models.TextChoices):
    """حالات الطلب"""
    DRAFT = 'draft', 'مسودة'
    NEW = 'new', 'جديد'
    IN_REVIEW = 'in_review', 'قيد المراجعة'
    APPROVED = 'approved', 'موافق عليه'
    PENDING_PAYMENT = 'pending_payment', 'بانتظار الدفع'
    PAID = 'paid', 'مدفوع'
    PROCESSING = 'processing', 'قيد التنفيذ'
    COMPLETED = 'completed', 'مكتمل'
    REJECTED = 'rejected', 'مرفوض'
    CANCELLED = 'cancelled', 'ملغي'
    ON_HOLD = 'on_hold', 'معلق'


class RequestCategory(models.Model):
    """فئات أنواع الطلبات (ديناميكية)"""
    
    name_arabic = models.CharField('الاسم بالعربية', max_length=100)
    name_english = models.CharField('الاسم بالإنجليزية', max_length=100, blank=True)
    code = models.CharField('الرمز', max_length=50, unique=True, editable=False)
    icon = models.CharField('الأيقونة', max_length=50, blank=True, default='', 
                           help_text='مثال: fa-file-alt (اختياري)')
    color = models.CharField('اللون', max_length=20, default='primary',
                            choices=[
                                ('primary', 'أزرق'),
                                ('success', 'أخضر'),
                                ('warning', 'أصفر'),
                                ('info', 'سماوي'),
                                ('danger', 'أحمر'),
                                ('secondary', 'رمادي'),
                            ])
    display_order = models.IntegerField('ترتيب العرض', default=0)
    is_active = models.BooleanField('نشط', default=True)
    
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    
    class Meta:
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'
        ordering = ['display_order', 'name_arabic']
    
    def __str__(self):
        return self.name_arabic
    
    def save(self, *args, **kwargs):
        # توليد الرمز تلقائياً من الاسم العربي
        if not self.code:
            import re
            # تحويل الاسم العربي إلى رمز إنجليزي
            code = re.sub(r'[^a-zA-Z0-9]', '_', self.name_english.lower() if self.name_english else self.name_arabic)
            code = re.sub(r'_+', '_', code).strip('_')
            self.code = code[:50]
        super().save(*args, **kwargs)


class RequestType(models.Model):
    """أنواع الطلبات (ديناميكية)"""
    
    # معلومات النوع
    name_arabic = models.CharField('الاسم بالعربية', max_length=200)
    name_english = models.CharField('الاسم بالإنجليزية', max_length=200, blank=True)
    code = models.CharField('الرمز', max_length=50, unique=True, editable=False)
    
    # الفئة (ديناميكية)
    category = models.ForeignKey(
        'RequestCategory',
        on_delete=models.PROTECT,
        related_name='request_types',
        verbose_name='الفئة',
        null=True,  # للتوافق المؤقت
        blank=True
    )
    
    # الوصف
    description = models.TextField('الوصف', blank=True)
    
    # الرسوم
    default_price = models.DecimalField('السعر الافتراضي', max_digits=10, decimal_places=2, default=420.00)
    
    # الحالة
    is_active = models.BooleanField('نشط', default=True)
    display_order = models.IntegerField('ترتيب العرض', default=0)
    
    # الإحصائيات
    usage_count = models.IntegerField('عدد الاستخدامات', default=0)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'نوع طلب'
        verbose_name_plural = 'أنواع الطلبات'
        ordering = ['display_order', 'name_arabic']
    
    def __str__(self):
        return self.name_arabic
    
    def save(self, *args, **kwargs):
        # توليد الرمز تلقائياً من الاسم
        if not self.code:
            import re
            from django.utils.text import slugify
            # استخدام الاسم الإنجليزي أو العربي
            base_name = self.name_english if self.name_english else self.name_arabic
            # تحويل إلى slug
            code = slugify(base_name).replace('-', '_')
            # التأكد من عدم التكرار
            original_code = code
            counter = 1
            while RequestType.objects.filter(code=code).exclude(pk=self.pk).exists():
                code = f"{original_code}_{counter}"
                counter += 1
            self.code = code[:50]
        super().save(*args, **kwargs)


class Request(models.Model):
    """طلب ربط الحساب"""
    
    # رقم مرجعي فريد
    reference_number = models.CharField(
        'الرقم المرجعي',
        max_length=20,
        unique=True,
        editable=False
    )  # QL-2025-001
    
    # العميل
    customer = models.ForeignKey(
        'clients.Customer',
        on_delete=models.PROTECT,
        related_name='requests',
        verbose_name='العميل'
    )
    
    # نوع الطلب (ديناميكي من Database)
    request_type = models.ForeignKey(
        'RequestType',
        on_delete=models.PROTECT,
        related_name='requests',
        verbose_name='نوع الطلب',
        null=True,  # للتوافق مع البيانات القديمة
        blank=True
    )
    
    # نوع الطلب القديم (للتوافق المؤقت - سيتم حذفه لاحقاً)
    request_type_legacy = models.CharField(
        'نوع الطلب (قديم)',
        max_length=100,
        blank=True,
        null=True
    )
    
    # الحالة
    status = models.CharField(
        'الحالة',
        max_length=20,
        choices=RequestStatus.choices,
        default=RequestStatus.NEW
    )
    
    # الأولوية
    priority = models.CharField('الأولوية', max_length=20, choices=[
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية'),
        ('urgent', 'عاجلة'),
    ], default='medium')
    
    # القالب القانوني المستخدم
    template = models.ForeignKey(
        'Template',
        on_delete=models.PROTECT,
        related_name='requests',
        verbose_name='القالب القانوني',
        null=True,
        blank=True
    )
    
    # الموافقة
    needs_approval = models.BooleanField('يحتاج موافقة', default=True)
    approved_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_requests',
        verbose_name='تمت الموافقة من'
    )
    approved_at = models.DateTimeField('تاريخ الموافقة', null=True, blank=True)
    
    # الرفض
    rejected_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rejected_requests',
        verbose_name='تم الرفض من'
    )
    rejected_at = models.DateTimeField('تاريخ الرفض', null=True, blank=True)
    rejection_reason = models.TextField('سبب الرفض', blank=True)
    
    # التواريخ المهمة
    submission_date = models.DateField('تاريخ التقديم', null=True, blank=True)
    due_date = models.DateField('تاريخ الاستحقاق', null=True, blank=True)
    completion_date = models.DateTimeField('تاريخ الإكمال', null=True, blank=True)
    
    # الدفع
    total_amount = models.DecimalField('المبلغ الإجمالي', max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField('مدفوع', default=False)
    payment_method = models.CharField('طريقة الدفع', max_length=50, blank=True)
    
    # البيانات الإضافية
    description = models.TextField('الوصف', blank=True)
    notes = models.TextField('ملاحظات', blank=True)
    internal_notes = models.TextField('ملاحظات داخلية', blank=True)
    
    # Checklist
    checklist_completed = models.BooleanField('Checklist مكتمل', default=False)
    identity_verified = models.BooleanField('الهوية موثقة', default=False)
    template_selected = models.BooleanField('القالب محدد', default=False)
    payment_confirmed = models.BooleanField('الدفع مؤكد', default=False)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='requests_created',
        verbose_name='تم الإنشاء بواسطة'
    )
    assigned_to = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests',
        verbose_name='مسند إلى'
    )
    
    # Soft Delete
    is_deleted = models.BooleanField('محذوف', default=False)
    deleted_at = models.DateTimeField('تاريخ الحذف', null=True, blank=True)
    deleted_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests_deleted',
        verbose_name='تم الحذف بواسطة'
    )
    
    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']
        permissions = [
            ('approve_request', 'يمكنه الموافقة على الطلبات'),
            ('reject_request', 'يمكنه رفض الطلبات'),
            ('can_delete_request', 'يمكنه حذف الطلبات'),
            ('view_all_requests', 'يمكنه رؤية جميع الطلبات'),
        ]
        indexes = [
            models.Index(fields=['reference_number']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.reference_number} - {self.customer.full_name}"
    
    def save(self, *args, **kwargs):
        # توليد رقم مرجعي تلقائياً
        if not self.reference_number:
            year = datetime.now().year
            last_request = Request.objects.filter(
                reference_number__startswith=f'QL-{year}'
            ).order_by('-reference_number').first()
            
            if last_request:
                last_num = int(last_request.reference_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.reference_number = f'QL-{year}-{new_num:03d}'
        
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """هل الطلب متأخر؟"""
        if self.due_date:
            return date.today() > self.due_date and self.status not in ['completed', 'cancelled']
        return False
    
    @property
    def days_pending(self):
        """عدد أيام الانتظار"""
        return (datetime.now().date() - self.created_at.date()).days


class Template(models.Model):
    """القوالب القانونية المركزية"""
    
    # معلومات القالب
    name = models.CharField('اسم القالب', max_length=200)
    name_english = models.CharField('الاسم بالإنجليزية', max_length=200, blank=True)
    code = models.CharField('الرمز', max_length=50, unique=True, editable=False)
    
    # المحتوى
    content_arabic = models.TextField('المحتوى بالعربية')
    content_english = models.TextField('المحتوى بالإنجليزية', blank=True)
    
    # الإصدار
    version = models.CharField('الإصدار', max_length=20, default='1.0')
    
    # النوع
    template_type = models.CharField('نوع القالب', max_length=100, choices=[
        ('authorization', 'تفويض ربط حساب'),
        ('service_agreement', 'اتفاقية الخدمة'),
        ('financial_contract', 'عقد الخدمات المالية'),
        ('customer_declaration', 'إقرار العميل'),
        ('privacy_policy', 'سياسة الخصوصية'),
        ('disclaimer', 'إخلاء المسؤولية'),
    ])
    
    # الحالة
    is_active = models.BooleanField('نشط', default=True)
    is_published = models.BooleanField('منشور', default=False)
    
    # الصلاحيات
    requires_admin_approval = models.BooleanField('يحتاج موافقة المشرف', default=True)
    
    # الملف المرفق
    file = models.FileField('ملف القالب', upload_to='templates/', blank=True)
    
    # الإحصائيات
    usage_count = models.IntegerField('عدد الاستخدامات', default=0)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'قالب'
        verbose_name_plural = 'القوالب'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """توليد الرمز تلقائياً من الاسم"""
        if not self.code:
            from django.utils.text import slugify
            # استخدام الاسم الإنجليزي أو العربي
            base_name = self.name_english or self.name
            base_code = slugify(base_name).replace('-', '_').upper()
            
            # التحقق من عدم التكرار
            counter = 1
            unique_code = base_code
            while Template.objects.filter(code=unique_code).exists():
                unique_code = f"{base_code}_{counter}"
                counter += 1
            
            self.code = unique_code
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} (v{self.version})"
    
    def increment_usage(self):
        """زيادة عدد الاستخدامات"""
        self.usage_count += 1
        self.save()
