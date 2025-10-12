# 🗄️ المرحلة 4: تصميم Database Models

## معلومات المرحلة

**رقم المرحلة**: 4  
**الاسم**: تصميم وإنشاء Database Models  
**الأولوية**: 🔴 عالية جداً  
**المدة المتوقعة**: 10-15 ساعة  
**تاريخ البدء**: اليوم  
**الحالة**: ⏳ **جاهز للبدء**

---

## 🎯 الأهداف

### الهدف الرئيسي:
**تصميم وإنشاء جميع Database Models للنظام**

### الأهداف الفرعية:
1. ✅ تصميم ERD Diagram
2. ✅ إنشاء Models لكل app
3. ✅ تحديد العلاقات بين Models
4. ✅ إضافة Validators
5. ✅ إنشاء Migrations
6. ✅ تفعيل Admin Panel

---

## 📊 الكيانات الأساسية (ERD)

### الكيانات الرئيسية (7):

```
┌─────────────┐       ┌──────────────┐       ┌────────────┐
│  Customer   │◄─────►│   Request    │◄─────►│  Payment   │
│  (العملاء)  │  1:N  │  (الطلبات)   │  1:1  │ (المدفوعات)│
└─────────────┘       └──────────────┘       └────────────┘
       │                      │                      │
       │                      │                      │
       │ 1:N                  │ 1:N                  │
       │                      │                      │
       ▼                      ▼                      │
┌─────────────┐       ┌──────────────┐              │
│IdentityIssue│       │ Attachment   │              │
│(التعارضات)  │       │  (المرفقات)  │              │
└─────────────┘       └──────────────┘              │
                             │                       │
                             │ N:1                   │
                             │                       │
                             ▼                       │
                      ┌──────────────┐              │
                      │  AuditLog    │◄─────────────┘
                      │(سجل التدقيق) │ 1:N
                      └──────────────┘
                             ▲
                             │ N:1
                             │
                      ┌──────────────┐       ┌──────────────┐
                      │     User     │◄─────►│   Template   │
                      │ (المستخدمين) │  N:N  │   (القوالب)  │
                      └──────────────┘       └──────────────┘
                             │
                             │ 1:N
                             ▼
                      ┌──────────────┐
                      │Notification  │
                      │ (الإشعارات)  │
                      └──────────────┘
```

---

## 📝 Models التفصيلية

### 1. Customer (العميل)
**App**: `apps/clients`

```python
from django.db import models
from django.core.validators import RegexValidator

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
    
    # معلومات إضافية
    occupation = models.CharField('المهنة', max_length=100, blank=True)
    company_name = models.CharField('اسم الشركة', max_length=200, blank=True)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='customers_created')
    
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
        return f"{self.emirates_id[:3]}-****-{self.emirates_id[8:15]}-{self.emirates_id[-1]}"
    
    @property
    def masked_phone(self):
        """رقم الجوال المخفي"""
        if len(self.phone) >= 10:
            return f"{self.phone[:3]}-****-{self.phone[-3:]}"
        return "****"
    
    @property
    def age(self):
        """حساب العمر"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def is_birthday_today(self):
        """هل اليوم عيد ميلاده؟"""
        from datetime import date
        today = date.today()
        return (today.month, today.day) == (self.date_of_birth.month, self.date_of_birth.day)
```

---

### 2. Request (الطلب)
**App**: `apps/requests`

```python
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
    
    # نوع الطلب
    request_type = models.CharField('نوع الطلب', max_length=100, choices=[
        ('paytabs_link', 'ربط حساب PayTabs'),
        ('payment_gateway', 'بوابة دفع'),
        ('merchant_account', 'حساب تاجر'),
        ('other', 'أخرى'),
    ])
    
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
        'requests.Template',
        on_delete=models.PROTECT,
        related_name='requests',
        verbose_name='القالب القانوني'
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
            ('delete_request', 'يمكنه حذف الطلبات'),
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
            from datetime import datetime
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
            from datetime import date
            return date.today() > self.due_date and self.status not in ['completed', 'cancelled']
        return False
    
    @property
    def days_pending(self):
        """عدد أيام الانتظار"""
        from datetime import datetime
        return (datetime.now().date() - self.created_at.date()).days
```

---

### 3. Template (القالب القانوني)
**App**: `apps/requests`

```python
class Template(models.Model):
    """القوالب القانونية المركزية"""
    
    # معلومات القالب
    name = models.CharField('اسم القالب', max_length=200)
    name_english = models.CharField('الاسم بالإنجليزية', max_length=200)
    code = models.CharField('الرمز', max_length=50, unique=True)
    
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
    
    def __str__(self):
        return f"{self.name} (v{self.version})"
    
    def increment_usage(self):
        """زيادة عدد الاستخدامات"""
        self.usage_count += 1
        self.save()
```

---

### 4. Payment (الدفع)
**App**: `apps/payments`

```python
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
    
    transaction_id = models.CharField('رقم المعاملة', max_length=100, blank=True)
    payment_url = models.URLField('رابط الدفع', blank=True)
    
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
    
    def __str__(self):
        return f"Payment for {self.request.reference_number} - {self.amount} {self.currency}"
    
    @property
    def is_paid(self):
        return self.status == 'paid'
    
    @property
    def is_refunded(self):
        return self.status == 'refunded'
```

---

### 5. AuditLog (سجل التدقيق)
**App**: `apps/audit`

```python
class AuditLog(models.Model):
    """سجل شامل لجميع العمليات"""
    
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
    
    # معلومات الجلسة
    ip_address = models.GenericIPAddressField('عنوان IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    
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
        ]
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"
```

---

### 6. Attachment (المرفق)
**App**: `apps/core_utils`

```python
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
```

---

### 7. Notification (الإشعار)
**App**: `apps/notifications`

```python
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
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        """وضع علامة مقروء"""
        from datetime import datetime
        self.is_read = True
        self.read_at = datetime.now()
        self.save()
```

---

### 8. SmartAlert (التنبيه الذكي)
**App**: `apps/notifications`

```python
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
```

---

### 9. ChatMessage (رسالة WhatsApp)
**App**: `apps/chat`

```python
class ChatMessage(models.Model):
    """رسائل WhatsApp Business"""
    
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
        verbose_name='المرسل'
    )
    
    # الحالة
    is_read = models.BooleanField('مقروء', default=False)
    read_at = models.DateTimeField('تاريخ القراءة', null=True, blank=True)
    
    # WhatsApp API Info
    whatsapp_message_id = models.CharField('WhatsApp Message ID', max_length=100, blank=True)
    
    # Metadata
    sent_at = models.DateTimeField('تاريخ الإرسال', auto_now_add=True)
    
    class Meta:
        verbose_name = 'رسالة'
        verbose_name_plural = 'الرسائل'
        ordering = ['sent_at']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.get_direction_display()} - {self.sent_at}"
```

---

### 10. IdentityConflict (تعارض الهوية)
**App**: `apps/clients`

```python
class IdentityConflict(models.Model):
    """كشف تعارضات الهوية"""
    
    # العملاء المتعارضون
    customer1 = models.ForeignKey(
        'clients.Customer',
        on_delete=models.CASCADE,
        related_name='conflicts_as_first',
        verbose_name='العميل الأول'
    )
    
    customer2 = models.ForeignKey(
        'clients.Customer',
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
```

---

### 11. UserProfile (ملف المستخدم)
**App**: `apps/accounts`

```python
class UserProfile(models.Model):
    """ملف المستخدم الممتد"""
    
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='المستخدم'
    )
    
    # معلومات إضافية
    employee_id = models.CharField('الرقم الوظيفي', max_length=50, unique=True)
    department = models.CharField('القسم', max_length=100)
    job_title = models.CharField('المسمى الوظيفي', max_length=100)
    phone = models.CharField('رقم الجوال', max_length=20)
    
    # الصورة
    avatar = models.ImageField('الصورة الشخصية', upload_to='avatars/', blank=True)
    
    # الدور
    role = models.CharField('الدور', max_length=20, choices=[
        ('admin', 'مشرف أعلى'),
        ('manager', 'مدير'),
        ('reviewer', 'مراجع'),
        ('intake', 'جامع بيانات'),
    ])
    
    # الإعدادات
    receive_email_notifications = models.BooleanField('إشعارات بريدية', default=True)
    receive_sms_notifications = models.BooleanField('إشعارات SMS', default=False)
    
    # آخر نشاط
    last_login_ip = models.GenericIPAddressField('آخر IP', null=True, blank=True)
    last_activity = models.DateTimeField('آخر نشاط', null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    
    class Meta:
        verbose_name = 'ملف مستخدم'
        verbose_name_plural = 'ملفات المستخدمين'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"
```

---

### 12. Backup (النسخة الاحتياطية)
**App**: `apps/core_utils`

```python
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
    
    # التواريخ
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
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
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
```

---

## 📋 ملخص Models

| App | Models | العدد |
|-----|--------|-------|
| **requests** | Request, Template | 2 |
| **clients** | Customer, IdentityConflict | 2 |
| **payments** | Payment | 1 |
| **audit** | AuditLog | 1 |
| **notifications** | Notification, SmartAlert | 2 |
| **chat** | ChatMessage | 1 |
| **accounts** | UserProfile | 1 |
| **core_utils** | Attachment, Backup | 2 |
| **إجمالي** | | **12 models** |

---

## 🚀 الخطوات التالية

### الخطوة 1: إنشاء Models (2 ساعات)
- [ ] إنشاء كل model في app الخاص به
- [ ] إضافة validators
- [ ] إضافة properties
- [ ] إضافة Meta options

### الخطوة 2: Migrations (30 دقيقة)
```bash
python manage.py makemigrations
python manage.py migrate
```

### الخطوة 3: Admin Panel (1 ساعة)
- [ ] تسجيل Models في admin.py
- [ ] إضافة list_display
- [ ] إضافة list_filter
- [ ] إضافة search_fields

### الخطوة 4: اختبار (30 دقيقة)
- [ ] إنشاء superuser
- [ ] إضافة بيانات تجريبية
- [ ] اختبار CRUD

---

**📅 تاريخ الإنشاء**: يناير 2025  
**👤 المسؤول**: فريق التطوير  
**📊 الحالة**: ⏳ جاهز للتنفيذ

