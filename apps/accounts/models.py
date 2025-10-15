from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """ملف المستخدم الممتد"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='المستخدم'
    )
    
    # معلومات إضافية
    employee_id = models.CharField('الرقم الوظيفي', max_length=50, unique=True, blank=True)
    department = models.CharField('القسم', max_length=100, blank=True)
    job_title = models.CharField('المسمى الوظيفي', max_length=100, blank=True)
    phone = models.CharField('رقم الجوال', max_length=20, blank=True)
    
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
    language = models.CharField('اللغة', max_length=10, choices=[
        ('ar', 'العربية'),
        ('en', 'English'),
    ], default='ar')
    
    # آخر نشاط
    last_login_ip = models.GenericIPAddressField('آخر IP', null=True, blank=True)
    last_activity = models.DateTimeField('آخر نشاط', null=True, blank=True)
    
    # الإحصائيات
    requests_handled = models.IntegerField('الطلبات المعالجة', default=0)
    customers_managed = models.IntegerField('العملاء المتابعين', default=0)
    
    # Metadata
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)
    
    # الحالة
    is_active = models.BooleanField('نشط', default=True)
    
    class Meta:
        verbose_name = 'ملف مستخدم'
        verbose_name_plural = 'ملفات المستخدمين'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"


# Signal لإنشاء UserProfile تلقائياً
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # توليد رقم وظيفي فريد
        import uuid
        employee_id = f"EMP-{uuid.uuid4().hex[:8].upper()}"
        
        # التأكد من عدم التكرار
        while UserProfile.objects.filter(employee_id=employee_id).exists():
            employee_id = f"EMP-{uuid.uuid4().hex[:8].upper()}"
        
        UserProfile.objects.create(
            user=instance,
            employee_id=employee_id,
            department='غير محدد',
            job_title='غير محدد',
            phone='غير محدد'
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
