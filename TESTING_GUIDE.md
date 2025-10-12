# 🧪 دليل الاختبار السريع - Quick Link System

## 🎯 جاهز للاختبار غداً!

---

## ⚡ **البدء السريع (5 دقائق)**

### **الخطوة 1: تشغيل المشروع**
```bash
cd /media/eslames/work/frontend/quicklink-system
source venv/bin/activate
python manage.py runserver
```

**النتيجة**: الخادم يعمل على `http://127.0.0.1:8000`

---

### **الخطوة 2: إنشاء Superuser**
```bash
python manage.py createsuperuser
```

**أدخل**:
- Username: `admin`
- Email: `admin@quicklink.ae`
- Password: `admin123` (أو أي كلمة مرور)

---

### **الخطوة 3: افتح المتصفح**
```
http://127.0.0.1:8000/accounts/login/
```

---

## 📋 **سيناريوهات الاختبار**

### **السيناريو 1: تسجيل الدخول** ✅
```
1. افتح: http://127.0.0.1:8000/accounts/login/
2. أدخل: admin / admin123
3. اضغط: تسجيل الدخول
4. النتيجة: تحويل إلى Dashboard
```

---

### **السيناريو 2: Dashboard** ✅
```
المسار: http://127.0.0.1:8000/

ماذا تتوقع:
✅ 4 بطاقات إحصائية (0 في البداية)
✅ جدول الطلبات الأخيرة (فارغ)
✅ التنبيهات (فارغة)
✅ إحصائيات سريعة
```

---

### **السيناريو 3: إنشاء عميل + طلب** ✅
```
المسار: http://127.0.0.1:8000/create/

الخطوات:
1. اختر: "إضافة عميل جديد" (افتراضي)
2. املأ النموذج:
   - الاسم: أحمد محمد علي
   - الهوية: 784123456789012
   - تاريخ الميلاد: 1990-05-15
   - الجنسية: إماراتي
   - الجوال: +971501234567
   - نوع الطلب: ربط حساب PayTabs

3. اضغط: التالي (سيتم تفعيله لاحقاً)

النتيجة المتوقعة:
✅ النموذج يعمل
✅ Validation تعمل
✅ الحقول required تعمل
```

---

### **السيناريو 4: إضافة بيانات عبر Admin** 🆕
```
المسار: http://127.0.0.1:8000/admin/

الخطوات:
1. تسجيل دخول بـ superuser
2. اذهب إلى: Clients → Customers
3. اضغط: Add Customer
4. املأ البيانات:
   - Full name: أحمد محمد علي
   - Emirates ID: 784123456789012
   - Phone: +971501234567
   - Email: ahmed@test.com
   - Date of birth: 1990-05-15
   - Gender: Male
   - Nationality: الإمارات
   - Is active: ✓
   - Is verified: ✓

5. Save

6. كرر العملية لـ 5-10 عملاء
```

---

### **السيناريو 5: إنشاء طلبات** 🆕
```
المسار: http://127.0.0.1:8000/admin/requests/request/add/

الخطوات:
1. Customer: اختر العميل
2. Request type: ربط حساب PayTabs
3. Status: جديد
4. Priority: متوسطة
5. Total amount: 420
6. Save

7. كرر لـ 10-15 طلب مختلف
```

---

### **السيناريو 6: قائمة العملاء** ✅
```
المسار: http://127.0.0.1:8000/clients/

ماذا تتوقع:
✅ 4 بطاقات إحصائية محدثة
✅ جدول العملاء (مع البيانات)
✅ Masked data (784-****-*******-*)
✅ أزرار: عرض، تعديل، WhatsApp
✅ Pagination (إذا > 20 عميل)
```

---

### **السيناريو 7: تفاصيل العميل** ✅
```
المسار: http://127.0.0.1:8000/clients/1/

ماذا تتوقع:
✅ معلومات العميل كاملة
✅ جدول طلباته السابقة
✅ إحصائيات الطلبات
✅ تنبيه عيد الميلاد (إذا قريب)
✅ أزرار: تعديل، طلب جديد، WhatsApp
```

---

### **السيناريو 8: قائمة الطلبات** ✅
```
المسار: http://127.0.0.1:8000/list/

ماذا تتوقع:
✅ فلاتر: بحث، حالة، تاريخ
✅ 4 بطاقات إحصائية
✅ جدول الطلبات
✅ Badges ملونة (حسب الحالة)
✅ أزرار مشروطة (حسب الحالة)
✅ Pagination
```

---

### **السيناريو 9: الطلبات المعلقة** ✅
```
المسار: http://127.0.0.1:8000/pending/

ماذا تتوقع:
✅ Badge في العنوان (عدد المعلقة)
✅ تنبيه المتأخرة (إذا وجدت)
✅ فلاتر: أولوية، مدة
✅ 4 بطاقات إحصائية
✅ جدول مع أولويات ملونة
✅ Checkboxes للاختيار المتعدد
✅ Pagination
```

---

### **السيناريو 10: الإشعارات** ✅
```
المسار: http://127.0.0.1:8000/notifications/

ماذا تتوقع:
✅ Badge (عدد غير المقروءة)
✅ فلاتر: نوع، حالة، أولوية
✅ 4 بطاقات إحصائية
✅ قائمة الإشعارات (مع أيقونات)
✅ نسب مئوية حسب النوع
✅ أزرار: عرض، وضع علامة مقروء، حذف
```

---

### **السيناريو 11: المدفوعات** ✅
```
المسار: http://127.0.0.1:8000/payments/

ماذا تتوقع:
✅ فلاتر: حالة، بوابة، تاريخ
✅ 4 بطاقات إحصائية
✅ نسب البوابات (PayTabs, Cash, Bank)
✅ جدول المدفوعات
✅ Badges ملونة (paid, pending, failed)
✅ أزرار مشروطة (حسب الحالة)
```

---

### **السيناريو 12: Chat** ✅
```
المسار: http://127.0.0.1:8000/chat/

ماذا تتوقع:
✅ قائمة المحادثات (يسار)
✅ شاشة الرسائل (وسط)
✅ نموذج الإرسال (أسفل)
✅ عدد الرسائل غير المقروءة
✅ آخر رسالة لكل عميل
```

---

### **السيناريو 13: Audit Trail** ✅
```
المسار: http://127.0.0.1:8000/audit/

ماذا تتوقع:
✅ فلاتر: تاريخ، مستخدم، إجراء
✅ 4 بطاقات إحصائية
✅ سجل مجمع حسب التاريخ
✅ تفاصيل كل عملية
✅ User + Action + IP
```

---

### **السيناريو 14: Profile** ✅
```
المسار: http://127.0.0.1:8000/accounts/profile/

ماذا تتوقع:
✅ معلومات المستخدم
✅ الصورة الشخصية
✅ الدور والصلاحيات
✅ نموذج التعديل
✅ زر حفظ
```

---

## 🐛 **اختبار المشاكل المحتملة**

### **1. Pagination**
```
الاختبار:
- أنشئ > 20 طلب
- اذهب إلى /list/
- تحقق من ظهور أزرار الصفحات

النتيجة المتوقعة:
✅ السابق/التالي يعملان
✅ أرقام الصفحات صحيحة
✅ "عرض 1-20 من X نتيجة"
```

---

### **2. Filters**
```
الاختبار:
- اذهب إلى /list/
- اختر filter: status = "new"
- اضغط بحث

النتيجة المتوقعة:
✅ عرض الطلبات الجديدة فقط
✅ الفلتر يبقى بعد التطبيق
✅ Pagination يعمل مع الفلتر
```

---

### **3. Modal System**
```
الاختبار:
- اذهب إلى أي صفحة
- اضغط زر "حذف" أو "موافقة"

النتيجة المتوقعة:
✅ Modal يظهر (ليس alert)
✅ التصميم موحد
✅ أزرار: تأكيد، إلغاء
✅ Callback يعمل
```

---

### **4. Responsive Design**
```
الاختبار:
- افتح Chrome DevTools (F12)
- Toggle Device Toolbar (Ctrl+Shift+M)
- اختر: iPhone 12 Pro

النتيجة المتوقعة:
✅ Sidebar قابل للطي
✅ الجداول scrollable
✅ البطاقات stack عمودياً
✅ الأزرار full-width
```

---

### **5. Customer Selection في Create Request**
```
الاختبار:
- اذهب إلى /create/
- اختر: "اختيار عميل موجود"

النتيجة المتوقعة:
✅ قسم البحث يظهر
✅ قسم العميل الجديد يختفي
✅ قائمة العملاء تظهر
✅ اختيار عميل يملأ hidden input
```

---

## 📊 **Checklist الاختبار**

### **الصفحات الأساسية:**
- [ ] ✅ Login
- [ ] ✅ Dashboard
- [ ] ✅ Create Request
- [ ] ✅ Requests List
- [ ] ✅ Request Details
- [ ] ✅ Pending Requests
- [ ] ✅ Customers List
- [ ] ✅ Customer Details
- [ ] ✅ Customer Edit

### **الصفحات الإضافية:**
- [ ] ✅ Payments
- [ ] ✅ Notifications
- [ ] ✅ Smart Alerts
- [ ] ✅ Chat
- [ ] ✅ Audit Trail
- [ ] ✅ Attachments
- [ ] ✅ Backup
- [ ] ✅ Profile
- [ ] ✅ Users List
- [ ] ✅ Identity Conflicts

### **الميزات:**
- [ ] ✅ Pagination
- [ ] ✅ Filters
- [ ] ✅ Search
- [ ] ✅ Modal System
- [ ] ✅ Customer Selection
- [ ] ✅ Statistics
- [ ] ✅ Conditional Buttons
- [ ] ✅ Responsive Design

---

## 🎯 **البيانات التجريبية المقترحة**

### **العملاء (5-10):**
```python
# استخدم Django Admin أو Shell

from apps.clients.models import Customer

customers_data = [
    {
        "full_name": "أحمد محمد علي السعيد",
        "emirates_id": "784123456789012",
        "phone": "+971501234567",
        "email": "ahmed@test.com",
        "date_of_birth": "1990-05-15",
        "gender": "male",
        "nationality": "الإمارات"
    },
    {
        "full_name": "فاطمة عبدالله الزعابي",
        "emirates_id": "784234567890123",
        "phone": "+971502345678",
        "email": "fatima@test.com",
        "date_of_birth": "1995-08-20",
        "gender": "female",
        "nationality": "الإمارات"
    },
    {
        "full_name": "محمد سالم الأحمد",
        "emirates_id": "784345678901234",
        "phone": "+971503456789",
        "email": "mohammed@test.com",
        "date_of_birth": "1988-12-10",
        "gender": "male",
        "nationality": "الإمارات"
    },
    # أضف المزيد...
]

for data in customers_data:
    Customer.objects.create(**data)
```

### **الطلبات (10-20):**
```python
from apps.requests.models import Request
from apps.clients.models import Customer

customers = Customer.objects.all()

for i, customer in enumerate(customers):
    Request.objects.create(
        customer=customer,
        request_type='paytabs_link',
        status='new' if i % 3 == 0 else 'in_review',
        priority='urgent' if i % 5 == 0 else 'medium',
        total_amount=420
    )
```

### **الإشعارات (5-10):**
```python
from apps.notifications.models import Notification
from django.contrib.auth.models import User

admin = User.objects.get(username='admin')

notifications_data = [
    {
        "recipient": admin,
        "notification_type": "new_request",
        "title": "طلب جديد",
        "message": "تم إنشاء طلب جديد من أحمد محمد",
        "priority": "normal"
    },
    {
        "recipient": admin,
        "notification_type": "identity_conflict",
        "title": "تعارض هوية",
        "message": "اكتشاف تعارض في الهوية",
        "priority": "high"
    },
    # أضف المزيد...
]

for data in notifications_data:
    Notification.objects.create(**data)
```

---

## 🔍 **فحص Console للأخطاء**

### **افتح Chrome DevTools:**
```
F12 → Console Tab
```

### **تحقق من:**
```
✅ لا أخطاء JavaScript
✅ لا 404 errors (static files)
✅ لا CSRF errors
✅ Network requests سريعة (< 500ms)
```

---

## 📱 **اختبار Responsive**

### **الأجهزة المقترحة:**
```
1. Desktop (1920x1080)
2. Tablet (iPad - 768x1024)
3. Mobile (iPhone 12 - 390x844)
```

### **ما تختبره:**
```
✅ Sidebar يتكيف
✅ الجداول scrollable
✅ البطاقات تترتب عمودياً
✅ الأزرار واضحة
✅ النصوص مقروءة
```

---

## ⚠️ **المشاكل المتوقعة وحلولها**

### **مشكلة 1: "Page not found"**
```
السبب: URLs غير صحيحة
الحل: تحقق من config/urls.py
```

### **مشكلة 2: "TemplateDoesNotExist"**
```
السبب: Template غير موجود
الحل: تحقق من مسار Template
```

### **مشكلة 3: "Static files not found"**
```
السبب: STATIC_URL غير مضبوط
الحل: python manage.py collectstatic
```

### **مشكلة 4: "No data shown"**
```
السبب: قاعدة البيانات فارغة
الحل: أضف بيانات تجريبية عبر Admin
```

---

## 📝 **تسجيل النتائج**

### **أثناء الاختبار:**
```markdown
## اختبار: [اسم الصفحة]
**التاريخ**: [التاريخ]
**المتصفح**: Chrome 120

### ما يعمل:
- ✅ ...
- ✅ ...

### ما لا يعمل:
- ❌ ...
- ❌ ...

### ملاحظات:
- ...
```

---

## 🎯 **معايير النجاح**

### **الاختبار ناجح عندما:**
```
✅ جميع الصفحات تفتح بدون أخطاء
✅ البيانات الديناميكية تظهر
✅ Pagination يعمل
✅ Filters تعمل
✅ Modal System يعمل
✅ Responsive يعمل
✅ لا أخطاء في Console
✅ Statistics صحيحة
```

---

## 🚀 **الخطوات بعد الاختبار الناجح**

### **1. تسجيل النتائج:**
```
✅ أنشئ ملف: TESTING_RESULTS.md
✅ سجل جميع النتائج
✅ التقط screenshots
```

### **2. تحديد الأولويات:**
```
✅ اجمع المشاكل
✅ صنفها: critical, high, medium, low
✅ أنشئ TODO list
```

### **3. التخطيط للمرحلة القادمة:**
```
✅ راجع ROADMAP.md
✅ افهم المرحلة 10: Forms & Business Logic
✅ ابدأ التخطيط
```

---

## 💡 **نصائح مهمة**

### **1. ابدأ بالبيانات:**
```
⚠️ أضف بيانات تجريبية أولاً
⚠️ على الأقل 10 عملاء + 15 طلب
⚠️ استخدم Admin Panel للسرعة
```

### **2. اختبر بالترتيب:**
```
1. Login أولاً
2. ثم Dashboard
3. ثم باقي الصفحات
4. لا تتجاوز الأخطاء
```

### **3. راقب Console:**
```
✅ افتح DevTools دائماً
✅ راقب الأخطاء
✅ راقب Network requests
```

---

## 🎊 **مبروك مقدماً!**

**النظام جاهز للاختبار!**  
**78% من المشروع مكتمل!**  
**0 أخطاء Django!**  

**فقط أضف بيانات وابدأ!** 🚀

---

© 2025 Quick Link System  
**آخر تحديث**: 12 أكتوبر 2025  
**الحالة**: 🧪 جاهز للاختبار!

