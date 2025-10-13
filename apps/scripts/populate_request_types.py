"""
Script لنقل أنواع الطلبات من CHOICES إلى Database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.requests.models import RequestType

# البيانات الأولية لأنواع الطلبات
REQUEST_TYPES_DATA = [
    # خدمات PayTabs
    {
        'name_arabic': 'ربط حساب PayTabs',
        'name_english': 'PayTabs Account Link',
        'code': 'paytabs_link',
        'category': 'paytabs',
        'description': 'خدمة ربط حساب العميل مع بوابة PayTabs للدفع الإلكتروني',
        'default_price': 420.00,
        'display_order': 1
    },
    {
        'name_arabic': 'تكامل PayTabs API',
        'name_english': 'PayTabs API Integration',
        'code': 'paytabs_integration',
        'category': 'paytabs',
        'description': 'تكامل API PayTabs مع موقع العميل',
        'default_price': 850.00,
        'display_order': 2
    },
    {
        'name_arabic': 'تحديث حساب PayTabs',
        'name_english': 'PayTabs Account Update',
        'code': 'paytabs_update',
        'category': 'paytabs',
        'description': 'تحديث بيانات حساب PayTabs الموجود',
        'default_price': 250.00,
        'display_order': 3
    },
    
    # بوابات الدفع
    {
        'name_arabic': 'بوابة دفع إلكترونية',
        'name_english': 'Payment Gateway',
        'code': 'payment_gateway',
        'category': 'payment_gateway',
        'description': 'إعداد بوابة دفع إلكترونية عامة',
        'default_price': 650.00,
        'display_order': 4
    },
    {
        'name_arabic': 'إعداد بوابة دفع',
        'name_english': 'Payment Gateway Setup',
        'code': 'payment_gateway_setup',
        'category': 'payment_gateway',
        'description': 'إعداد وتكوين بوابة الدفع',
        'default_price': 550.00,
        'display_order': 5
    },
    {
        'name_arabic': 'نقل بوابة دفع',
        'name_english': 'Payment Gateway Migration',
        'code': 'payment_gateway_migration',
        'category': 'payment_gateway',
        'description': 'نقل من بوابة دفع إلى أخرى',
        'default_price': 750.00,
        'display_order': 6
    },
    
    # حسابات تجارية
    {
        'name_arabic': 'حساب تاجر',
        'name_english': 'Merchant Account',
        'code': 'merchant_account',
        'category': 'merchant',
        'description': 'إنشاء حساب تاجر جديد',
        'default_price': 500.00,
        'display_order': 7
    },
    {
        'name_arabic': 'توثيق حساب تاجر',
        'name_english': 'Merchant Verification',
        'code': 'merchant_verification',
        'category': 'merchant',
        'description': 'توثيق والتحقق من حساب التاجر',
        'default_price': 300.00,
        'display_order': 8
    },
    {
        'name_arabic': 'ترقية حساب تاجر',
        'name_english': 'Merchant Upgrade',
        'code': 'merchant_upgrade',
        'category': 'merchant',
        'description': 'ترقية حساب التاجر لمستوى أعلى',
        'default_price': 400.00,
        'display_order': 9
    },
    
    # تكاملات بنكية
    {
        'name_arabic': 'تكامل بنكي',
        'name_english': 'Bank Integration',
        'code': 'bank_integration',
        'category': 'bank',
        'description': 'تكامل مع النظام البنكي',
        'default_price': 900.00,
        'display_order': 10
    },
    {
        'name_arabic': 'ربط حساب بنكي',
        'name_english': 'Bank Account Link',
        'code': 'bank_account_link',
        'category': 'bank',
        'description': 'ربط الحساب البنكي مع النظام',
        'default_price': 600.00,
        'display_order': 11
    },
    {
        'name_arabic': 'إعداد تحويل بنكي',
        'name_english': 'Bank Transfer Setup',
        'code': 'bank_transfer_setup',
        'category': 'bank',
        'description': 'إعداد نظام التحويلات البنكية',
        'default_price': 700.00,
        'display_order': 12
    },
    
    # خدمات إضافية
    {
        'name_arabic': 'جهاز نقاط البيع (POS)',
        'name_english': 'POS Terminal',
        'code': 'pos_terminal',
        'category': 'additional',
        'description': 'توفير وإعداد جهاز نقاط البيع',
        'default_price': 1200.00,
        'display_order': 13
    },
    {
        'name_arabic': 'الدفع عبر الجوال',
        'name_english': 'Mobile Payment',
        'code': 'mobile_payment',
        'category': 'additional',
        'description': 'تفعيل خدمة الدفع عبر الجوال',
        'default_price': 450.00,
        'display_order': 14
    },
    {
        'name_arabic': 'خدمة اشتراكات',
        'name_english': 'Subscription Service',
        'code': 'subscription_service',
        'category': 'additional',
        'description': 'إعداد نظام الاشتراكات الدورية',
        'default_price': 800.00,
        'display_order': 15
    },
    {
        'name_arabic': 'خدمة المرتجعات',
        'name_english': 'Refund Service',
        'code': 'refund_service',
        'category': 'additional',
        'description': 'إعداد نظام المرتجعات والاستردادات',
        'default_price': 350.00,
        'display_order': 16
    },
    
    # أخرى
    {
        'name_arabic': 'استشارة فنية',
        'name_english': 'Technical Consultation',
        'code': 'consultation',
        'category': 'other',
        'description': 'استشارة فنية متخصصة',
        'default_price': 200.00,
        'display_order': 17
    },
    {
        'name_arabic': 'طلب دعم فني',
        'name_english': 'Technical Support',
        'code': 'support_request',
        'category': 'other',
        'description': 'طلب دعم فني',
        'default_price': 150.00,
        'display_order': 18
    },
    {
        'name_arabic': 'حل مخصص',
        'name_english': 'Custom Solution',
        'code': 'custom_solution',
        'category': 'other',
        'description': 'حل مخصص حسب احتياجات العميل',
        'default_price': 1500.00,
        'display_order': 19
    },
    {
        'name_arabic': 'أخرى',
        'name_english': 'Other',
        'code': 'other',
        'category': 'other',
        'description': 'خدمات أخرى',
        'default_price': 420.00,
        'display_order': 20
    },
]


def populate_request_types():
    """إضافة أنواع الطلبات إلى Database"""
    print("🚀 بدء إضافة أنواع الطلبات...")
    
    created_count = 0
    skipped_count = 0
    
    for data in REQUEST_TYPES_DATA:
        # التحقق من عدم وجود النوع
        if RequestType.objects.filter(code=data['code']).exists():
            print(f"⏭️  تخطي: {data['name_arabic']} (موجود مسبقاً)")
            skipped_count += 1
            continue
        
        # إنشاء النوع
        request_type = RequestType.objects.create(**data)
        print(f"✅ تم إنشاء: {request_type.name_arabic} ({request_type.code})")
        created_count += 1
    
    print(f"\n📊 النتيجة:")
    print(f"   ✅ تم إنشاء: {created_count} نوع")
    print(f"   ⏭️  تم تخطي: {skipped_count} نوع (موجود مسبقاً)")
    print(f"   📦 الإجمالي: {RequestType.objects.count()} نوع في Database")
    print(f"\n🎉 تم بنجاح!")


if __name__ == '__main__':
    populate_request_types()

