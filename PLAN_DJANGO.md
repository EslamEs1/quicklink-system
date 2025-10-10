## خطة تنفيذ Quick Link System باستخدام Django + HTML/CSS/Bootstrap

### 1) النطاق والافتراضات
- لا نستخدم Django Forms أو JS للتحقق؛ التحقق سيكون في طبقة النماذج (Models) والـViews.
- واجهات HTML تعتمد Bootstrap 5 فقط، مع `custom.css` و`custom.js` موحّدين.
- إعادة استخدام تخطيطات رئيسية من `index.html` والمكوّنات المشتركة.

### 2) هيكلة المشروع
- مشروع: `quicklink/`
  - تطبيقات:
    1. `accounts` لإدارة المستخدمين والأدوار.
    2. `customers` لملفات العملاء.
    3. `requests` لإدارة طلبات الربط والدفع والمرفقات.
    4. `legal` لقوالب التفويض/التوكيلات وإصداراتها.
    5. `audit` لسجل التدقيق.
    6. `notifications` للتنبيهات والمهام.
    7. `payments` للتكامل مع بوابة الدفع (PayTabs أو بديل).

هيكل عام:
```
quicklink/
  manage.py
  quicklink/settings.py
  quicklink/urls.py
  static/{css/custom.css, js/custom.js, img/}
  templates/{base.html, navbar.html, sidebar.html, index.html}
  apps/
    accounts/
    customers/
    requests/
    legal/
    audit/
    notifications/
    payments/
```

### 3) نماذج البيانات الأساسية (Models)
- accounts.User (يمدّد AbstractUser) مع حقول: role, can_view_masked_phone, ...
- customers.Customer: national_id, full_name, birth_date, phone, email, status.
- requests.QuickLinkRequest: ref_code, customer(FK), type, status, amount, paid_at, payment_ref, reviewer(FK), intake_user(FK), manager_note.
- requests.Attachment: request(FK), file, kind, version, checksum, is_encrypted.
- legal.Template: code, title, version, is_active, file.
- audit.AuditLog: actor(FK User), entity_type, entity_id, action, old_values(JSON), new_values(JSON), at.
- notifications.Notification: recipient(FK User), kind, message, is_read, related_request(FK), created_at.

قواعد تحقق رئيسية داخل Models:
- national_id pattern: 15 رقمًا بصيغة محددة (مثل 784-XXXX-XXXXXXX-X) مع دوال تحقق.
- منع تعديل الطلب بعد `paid_at` ليس Null.
- حماية الهاتف: إرجاع masked value افتراضيًا إلا لمن يملك صلاحية.
- قيد فريد: ref_code فريد لكل طلب؛ لكل عميل عدة طلبات مع تسلسل زمني.

### 4) الصلاحيات والأدوار
- Intake: إنشاء/تعديل مسودات الطلبات قبل الدفع؛ رؤية العملاء الذين أنشأهم.
- Reviewer: مراجعة، تفعيل، اعتماد التفويضات، تحديث الحالة.
- Manager: رؤية جميع الطلبات والعملاء؛ تقارير؛ إدارة القوالب.
- Admin: كل الصلاحيات.

سياسة الوصول للبيانات:
- فلترة تلقائية على مستوى QuerySet بحسب الدور.
- إخفاء الهاتف بالكامل؛ إظهار زر اتصال فقط (ينفّذ اتصال/واتساب من النظام بدون كشف الرقم بالكامل).

### 5) مسارات العمل (Workflows)
1. إنشاء عميل جديد → تحقق من الهوية والاسم وتاريخ الميلاد.
2. إنشاء طلب جديد للعميل → توليد `ref_code` مثل `QL-2025-001`.
3. رفع المرفقات عبر قوالب مركزية/Checklist.
4. دفع الرسوم مركزيًا عبر `payments` → تخزين `payment_ref` وتجميد التعديل.
5. مراجعة واعتماد الطلب من Reviewer.
6. إغلاق الطلب أو طلب استكمال مع تنبيهات.

حالات الطلب: draft → pending_payment → paid → under_review → completed | rejected | needs_more_info.

### 6) التكامل مع الدفع
- واجهة خدمة `PaymentGateway` مع تنفيذ `PayTabsService` لاحقًا.
- أساليب: create_payment_link(amount, ref_code), verify_callback(payload).
- Webhook endpoint مع توقيع/سر.

### 7) سجل التدقيق
- ديكوريتر/ميدلوير يسجّل تلقائيًا أي create/update/delete على الكيانات الحساسة.
- تخزين الفرق في JSON مع حدود حجم ومحو أرشيفي دوري.

### 8) التنبيهات
- إشعارات عند: مرور 24 ساعة دون فتح الطلب، تعارض هوية، اسم مطابق لهوية مختلفة، تأخير مراجعة.
- قنوات: داخل النظام + بريد لاحقًا.

### 9) الأمان والنسخ الاحتياطي
- تخزين المرفقات مشفّرًا على القرص مع مفاتيح خدمة النظام.
- نسخ احتياطي يومي إلى تخزين سحابي (S3/Google Drive API) بتهيئة بيئية.
- منع زر "نسخ" و"تصدير" للبيانات الحساسة؛ تسجيل محاولات الوصول.

### 10) الصفحات والقوالب (بدون JS تحقق)
- Customers: قائمة، إنشاء/تعديل، ملف عميل.
- Requests: إنشاء/تعديل قبل الدفع، صفحة دفع، مراجعة، تفاصيل كاملة.
- Legal Templates: إدارة القوالب والإصدارات.
- Audit: تقارير حسب الفترة والكيان.
- Dashboard: إحصاءات أساسية.

كل الصفحات تستخدم `base.html` مع `navbar.html` و`sidebar.html` وملفات `custom.css` و`custom.js` موحّدة.

### 11) خطة التنفيذ على مراحل
مرحلة A: إعداد المشروع والنماذج والهجرة الأولى.
مرحلة B: CRUD العملاء والطلبات مع Checklist.
مرحلة C: الدفع والتجميد بعد الدفع.
مرحلة D: الأدوار والصلاحيات وإخفاء الهاتف.
مرحلة E: سجل التدقيق والتنبيهات.
مرحلة F: النسخ الاحتياطي والتخزين المشفّر والتقارير.

### 12) أوامر إنشاء سريعة (للتنفيذ لاحقًا)
```
django-admin startproject quicklink .
python manage.py startapp accounts apps/accounts
python manage.py startapp customers apps/customers
python manage.py startapp requests apps/requests
python manage.py startapp legal apps/legal
python manage.py startapp audit apps/audit
python manage.py startapp notifications apps/notifications
python manage.py startapp payments apps/payments
```

### 13) ما تم وما التالي
- بعد الموافقة: سننشئ الهيكل الأساسي والملفات المشتركة، ثم نطبق مرحلة A.


