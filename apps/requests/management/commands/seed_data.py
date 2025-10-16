"""
Management command لإضافة البيانات التجريبية للنظام
python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from apps.requests.models import RequestCategory, RequestType, TemplateType, Template


class Command(BaseCommand):
    help = 'إضافة البيانات التجريبية للنظام'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 بدء إضافة البيانات التجريبية...'))
        
        # 1. إنشاء فئات الطلبات
        self.create_request_categories()
        
        # 2. إنشاء أنواع القوالب
        self.create_template_types()
        
        # 3. إنشاء أنواع الطلبات
        self.create_request_types()
        
        # 4. إنشاء القوالب
        self.create_templates()
        
        self.stdout.write(self.style.SUCCESS('✅ تم إضافة البيانات التجريبية بنجاح!'))

    def create_request_categories(self):
        """إنشاء فئات الطلبات"""
        self.stdout.write('📁 إنشاء فئات الطلبات...')
        
        categories_data = [
            {
                'name_arabic': 'خدمات قانونية',
                'name_english': 'Legal Services',
                'icon': 'fa-gavel',
                'color': 'primary',
                'display_order': 1
            },
            {
                'name_arabic': 'خدمات مالية',
                'name_english': 'Financial Services',
                'icon': 'fa-money-bill-wave',
                'color': 'success',
                'display_order': 2
            },
            {
                'name_arabic': 'خدمات الربط',
                'name_english': 'Integration Services',
                'icon': 'fa-link',
                'color': 'info',
                'display_order': 3
            }
        ]
        
        for cat_data in categories_data:
            category, created = RequestCategory.objects.get_or_create(
                name_arabic=cat_data['name_arabic'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'  ✅ تم إنشاء الفئة: {category.name_arabic}')
            else:
                self.stdout.write(f'  ℹ️ الفئة موجودة: {category.name_arabic}')

    def create_template_types(self):
        """إنشاء أنواع القوالب"""
        self.stdout.write('📋 إنشاء أنواع القوالب...')
        
        template_types_data = [
            {
                'name_arabic': 'عقد ربط شركة',
                'name_english': 'Company Integration Contract',
                'icon': 'fa-building',
                'color': 'primary',
                'description': 'قوالب خاصة بربط حسابات الشركات',
                'display_order': 1
            },
            {
                'name_arabic': 'عقد ربط فرد',
                'name_english': 'Individual Integration Contract',
                'icon': 'fa-user',
                'color': 'info',
                'description': 'قوالب خاصة بربط حسابات الأفراد',
                'display_order': 2
            },
            {
                'name_arabic': 'تفويض قانوني',
                'name_english': 'Legal Authorization',
                'icon': 'fa-certificate',
                'color': 'success',
                'description': 'قوالب التفويضات القانونية',
                'display_order': 3
            }
        ]
        
        for tt_data in template_types_data:
            template_type, created = TemplateType.objects.get_or_create(
                name_arabic=tt_data['name_arabic'],
                defaults=tt_data
            )
            if created:
                self.stdout.write(f'  ✅ تم إنشاء نوع القالب: {template_type.name_arabic}')
            else:
                self.stdout.write(f'  ℹ️ نوع القالب موجود: {template_type.name_arabic}')

    def create_request_types(self):
        """إنشاء أنواع الطلبات"""
        self.stdout.write('📝 إنشاء أنواع الطلبات...')
        
        # الحصول على الفئات
        legal_category = RequestCategory.objects.get(name_arabic='خدمات قانونية')
        financial_category = RequestCategory.objects.get(name_arabic='خدمات مالية')
        integration_category = RequestCategory.objects.get(name_arabic='خدمات الربط')
        
        request_types_data = [
            {
                'name_arabic': 'طلب ربط شركة',
                'name_english': 'Company Integration Request',
                'category': integration_category,
                'default_price': 450.00,
                'description': 'طلب ربط حساب شركة مع النظام',
                'display_order': 1
            },
            {
                'name_arabic': 'طلب ربط فرد',
                'name_english': 'Individual Integration Request',
                'category': integration_category,
                'default_price': 300.00,
                'description': 'طلب ربط حساب فرد مع النظام',
                'display_order': 2
            },
            {
                'name_arabic': 'تفويض قانوني',
                'name_english': 'Legal Authorization',
                'category': legal_category,
                'default_price': 250.00,
                'description': 'إنشاء تفويض قانوني إلكتروني',
                'display_order': 3
            },
            {
                'name_arabic': 'مراجعة عقد',
                'name_english': 'Contract Review',
                'category': legal_category,
                'default_price': 200.00,
                'description': 'مراجعة وتدقيق العقود القانونية',
                'display_order': 4
            },
            {
                'name_arabic': 'فتح حساب تجاري',
                'name_english': 'Business Account Opening',
                'category': financial_category,
                'default_price': 500.00,
                'description': 'فتح حساب تجاري جديد',
                'display_order': 5
            }
        ]
        
        for rt_data in request_types_data:
            request_type, created = RequestType.objects.get_or_create(
                name_arabic=rt_data['name_arabic'],
                defaults=rt_data
            )
            if created:
                self.stdout.write(f'  ✅ تم إنشاء نوع الطلب: {request_type.name_arabic} - {request_type.default_price} درهم')
            else:
                self.stdout.write(f'  ℹ️ نوع الطلب موجود: {request_type.name_arabic}')

    def create_templates(self):
        """إنشاء القوالب"""
        self.stdout.write('📄 إنشاء القوالب...')
        
        # الحصول على أنواع القوالب
        company_template_type = TemplateType.objects.get(name_arabic='عقد ربط شركة')
        individual_template_type = TemplateType.objects.get(name_arabic='عقد ربط فرد')
        legal_template_type = TemplateType.objects.get(name_arabic='تفويض قانوني')
        
        templates_data = [
            {
                'name': 'عقد ربط حساب شركة',
                'name_english': 'Company Account Linking Contract',
                'template_type': company_template_type,
                'content_arabic': '''
                    عقد ربط الحساب للشركات
                    
                    هذا العقد يخول الشركة ربط حسابها مع النظام الإلكتروني.
                    
                    البنود الأساسية:
                    1. بيانات الشركة الكاملة
                    2. صلاحيات الممثل القانوني
                    3. التزامات الأمان والحماية
                    4. شروط الاستخدام
                    
                    تاريخ التوقيع: ___________
                    توقيع الممثل القانوني: ___________
                ''',
                'content_english': '''
                    Company Account Linking Contract
                    
                    This contract authorizes the company to link its account with the electronic system.
                    
                    Basic Terms:
                    1. Complete company data
                    2. Legal representative powers
                    3. Security and protection obligations
                    4. Terms of use
                    
                    Signature Date: ___________
                    Legal Representative Signature: ___________
                ''',
                'version': '1.0',
                'is_published': True
            },
            {
                'name': 'عقد ربط حساب فرد',
                'name_english': 'Individual Account Linking Contract',
                'template_type': individual_template_type,
                'content_arabic': '''
                    عقد ربط الحساب للأفراد
                    
                    هذا العقد يخول الشخص ربط حسابه مع النظام الإلكتروني.
                    
                    البنود الأساسية:
                    1. بيانات الهوية الشخصية
                    2. إثبات الهوية
                    3. التزامات الأمان
                    4. شروط الاستخدام
                    
                    تاريخ التوقيع: ___________
                    توقيع العميل: ___________
                ''',
                'content_english': '''
                    Individual Account Linking Contract
                    
                    This contract authorizes the individual to link their account with the electronic system.
                    
                    Basic Terms:
                    1. Personal identification data
                    2. Identity verification
                    3. Security obligations
                    4. Terms of use
                    
                    Signature Date: ___________
                    Customer Signature: ___________
                ''',
                'version': '1.0',
                'is_published': True
            },
            {
                'name': 'تفويض قانوني إلكتروني',
                'name_english': 'Electronic Legal Authorization',
                'template_type': legal_template_type,
                'content_arabic': '''
                    تفويض قانوني إلكتروني
                    
                    أنا الموقع أدناه أفوّض شركة كويك لينك للقيام بالعمليات التالية:
                    
                    1. ربط الحساب مع النظام الإلكتروني
                    2. تنفيذ المعاملات المالية
                    3. الحصول على البيانات المطلوبة
                    
                    هذا التفويض ساري المفعول حتى تاريخ: ___________
                    
                    توقيع المفوّض: ___________
                    تاريخ التوقيع: ___________
                ''',
                'content_english': '''
                    Electronic Legal Authorization
                    
                    I, the undersigned, authorize Quick Link Company to perform the following operations:
                    
                    1. Link account with electronic system
                    2. Execute financial transactions
                    3. Obtain required data
                    
                    This authorization is valid until: ___________
                    
                    Authorized Person Signature: ___________
                    Signature Date: ___________
                ''',
                'version': '1.0',
                'is_published': True
            }
        ]
        
        for template_data in templates_data:
            template, created = Template.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'  ✅ تم إنشاء القالب: {template.name} (v{template.version})')
            else:
                self.stdout.write(f'  ℹ️ القالب موجود: {template.name}')
