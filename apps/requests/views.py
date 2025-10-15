from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from .models import Request, Template
from apps.clients.models import Customer
from apps.payments.models import Payment
from datetime import datetime, date


# @login_required
def dashboard(request):
    """لوحة التحكم الرئيسية"""
    from django.db.models import Count, Q
    from apps.audit.models import AuditLog
    
    # إحصائيات الطلبات
    total_requests = Request.objects.filter(is_deleted=False).count()
    pending_requests = Request.objects.filter(
        status__in=['new', 'in_review', 'pending_payment'], 
        is_deleted=False
    ).count()
    
    # إحصائيات العملاء
    total_customers = Customer.objects.filter(is_active=True).count()
    
    # سجل التدقيق
    audit_logs_count = AuditLog.objects.count()
    
    # الطلبات الأخيرة مع بيانات العميل
    recent_requests = Request.objects.filter(
        is_deleted=False
    ).select_related('customer', 'created_by').order_by('-created_at')[:10]
    
    # طلبات اليوم
    today_requests = Request.objects.filter(
        created_at__date=date.today(),
        is_deleted=False
    ).count()
    
    # معدل الإنجاز
    completed_requests = Request.objects.filter(status='completed', is_deleted=False).count()
    completion_rate = round((completed_requests / total_requests * 100), 1) if total_requests > 0 else 0
    
    # الإشعارات الأخيرة
    from apps.notifications.models import Notification
    recent_notifications = Notification.objects.filter(
        is_read=False
    ).order_by('-created_at')[:3]
    
    context = {
        'page_title': 'لوحة التحكم',
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'total_customers': total_customers,
        'audit_logs_count': audit_logs_count,
        'recent_requests': recent_requests,
        'today_requests': today_requests,
        'completion_rate': completion_rate,
        'recent_notifications': recent_notifications,
    }
    return render(request, 'requests/dashboard.html', context)


# @login_required
def create(request):
    """إنشاء طلب جديد"""
    if request.method == 'POST':
        print("🚀 POST request received")
        print("📝 POST data:", request.POST)
        print("📁 FILES data:", request.FILES)
        try:
            # التحقق من خيار العميل
            existing_customer_id = request.POST.get('existing_customer_id')
            
            if existing_customer_id:
                # استخدام عميل موجود
                print("👤 Using existing customer:", existing_customer_id)
                customer = get_object_or_404(Customer, pk=existing_customer_id)
                customer_created = False
            else:
                # إنشاء عميل جديد
                full_name = request.POST.get('customerName')
                emirates_id = request.POST.get('emiratesId')
                phone = request.POST.get('mobileNumber')
                email = request.POST.get('email', '')
                date_of_birth = request.POST.get('date_of_birth')
                gender = request.POST.get('gender', 'male')
                nationality = request.POST.get('nationality', 'الإمارات')
                
                print("👤 Creating new customer:")
                print("  - Name:", full_name)
                print("  - Emirates ID:", emirates_id)
                print("  - Phone:", phone)
                print("  - Email:", email)
                print("  - DOB:", date_of_birth)
                print("  - Gender:", gender)
                print("  - Nationality:", nationality)
                
                # التحقق من عدم وجود نفس رقم الهوية
                if Customer.objects.filter(emirates_id=emirates_id).exists():
                    print("❌ Emirates ID already exists:", emirates_id)
                    messages.error(request, 'رقم الهوية موجود مسبقاً! استخدم "اختيار عميل موجود"')
                    return redirect('requests:create')
                
                # التحقق من البيانات المطلوبة
                if not full_name or not emirates_id or not phone or not date_of_birth:
                    print("❌ Missing required fields:")
                    print("  - Full Name:", full_name)
                    print("  - Emirates ID:", emirates_id)
                    print("  - Phone:", phone)
                    print("  - Date of Birth:", date_of_birth)
                    messages.error(request, 'يرجى ملء جميع الحقول المطلوبة')
                    return redirect('requests:create')
                
                # إنشاء العميل
                customer = Customer.objects.create(
                    full_name=full_name,
                    emirates_id=emirates_id,
                    phone=phone,
                    email=email,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    nationality=nationality,
                    created_by=request.user if request.user.is_authenticated else None,
                )
                print("✅ Customer created successfully:", customer.id)
                customer_created = True
            
            # الحصول على نوع الطلب
            request_type_id = request.POST.get('request_type_id')
            template_id = request.POST.get('template_id')
            payment_method = request.POST.get('paymentMethod', 'paytabs')
            
            print("📋 Request details:")
            print("  - Request Type ID:", request_type_id)
            print("  - Template ID:", template_id)
            print("  - Payment Method:", payment_method)
            
            # حساب المبلغ من نوع الطلب
            from apps.requests.models import RequestType
            request_type_instance = None
            total_amount = 0
            
            if request_type_id:
                request_type_instance = get_object_or_404(RequestType, pk=request_type_id)
                base_price = float(request_type_instance.default_price)
                tax = base_price * 0.05  # 5% ضريبة
                total_amount = base_price + tax
                print("💰 Pricing:")
                print("  - Base Price:", base_price)
                print("  - Tax:", tax)
                print("  - Total:", total_amount)
            
            # الحصول على الأولوية وتاريخ الاستحقاق
            priority = request.POST.get('priority', 'medium')
            due_date = request.POST.get('due_date', None)
            
            print("⏰ Priority & Due Date:")
            print("  - Priority:", priority)
            print("  - Due Date:", due_date)
            
            # إنشاء الطلب
            new_request = Request.objects.create(
                customer=customer,
                request_type=request_type_instance,  # ForeignKey للنوع
                priority=priority,
                due_date=due_date if due_date else None,
                total_amount=total_amount,
                description=request.POST.get('description', ''),
                created_by=request.user if request.user.is_authenticated else None,
            )
            print("✅ Request created successfully:", new_request.id, new_request.reference_number)
            
            # ربط القالب إذا تم اختياره
            if template_id:
                template = get_object_or_404(Template, pk=template_id)
                new_request.template = template
                new_request.save()
            
            # معالجة الدفع
            if payment_method == 'cash':
                receipt_number = request.POST.get('receiptNumber', '')
                # يمكن إنشاء سجل دفع هنا
                Payment.objects.create(
                    request=new_request,
                    amount=total_amount,
                    payment_method='cash',
                    receipt_number=receipt_number,
                    status='pending'
                )
            
            # رسالة نجاح
            if customer_created:
                messages.success(request, f'✅ تم إنشاء ملف العميل "{customer.full_name}" والطلب بنجاح! الرقم المرجعي: {new_request.reference_number}')
            else:
                messages.success(request, f'✅ تم إنشاء الطلب بنجاح للعميل "{customer.full_name}"! الرقم المرجعي: {new_request.reference_number}')
            
            # إعادة التوجيه إلى صفحة تفاصيل الطلب
            return redirect('requests:detail', pk=new_request.pk)
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ خطأ في إنشاء الطلب: {error_details}")  # للتشخيص في Console
            messages.error(request, f'❌ حدث خطأ: {str(e)}')
            return redirect('requests:create')
    
    # GET request - جلب قائمة العملاء للاختيار
    customers = Customer.objects.filter(is_active=True).order_by('-updated_at')[:50]
    templates = Template.objects.filter(is_active=True, is_published=True).order_by('template_type', 'name')
    
    # جلب أنواع الطلبات من Database (ديناميكي 100%)
    from apps.requests.models import RequestType
    request_types = RequestType.objects.filter(is_active=True).select_related('category').order_by('category__display_order', 'display_order')
    
    context = {
        'page_title': 'إنشاء طلب جديد',
        'templates': templates,
        'customers': customers,
        'request_types': request_types,  # أنواع الطلبات من Database
    }
    return render(request, 'requests/create.html', context)


# @login_required
def list(request):
    """جميع الطلبات"""
    from django.db.models import Sum
    
    # الفلاتر
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')
    date_filter = request.GET.get('date')
    
    # Query
    requests_list = Request.objects.filter(is_deleted=False).select_related(
        'customer', 'created_by', 'template'
    )
    
    if status_filter and status_filter != 'all':
        requests_list = requests_list.filter(status=status_filter)
    
    if search_query:
        requests_list = requests_list.filter(
            models.Q(reference_number__icontains=search_query) |
            models.Q(customer__full_name__icontains=search_query)
        )
    
    if date_filter:
        requests_list = requests_list.filter(created_at__date=date_filter)
    
    requests_list = requests_list.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(requests_list, 20)  # 20 طلب لكل صفحة
    page = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # إحصائيات
    total_count = Request.objects.filter(is_deleted=False).count()
    pending_count = Request.objects.filter(
        status__in=['new', 'in_review'], 
        is_deleted=False
    ).count()
    completed_count = Request.objects.filter(status='completed', is_deleted=False).count()
    
    # إجمالي الإيرادات
    total_revenue = Payment.objects.filter(status='paid').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    context = {
        'page_title': 'جميع الطلبات',
        'page_obj': page_obj,
        'total_count': total_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'total_revenue': total_revenue,
    }
    return render(request, 'requests/list.html', context)


# @login_required
def detail(request, pk):
    """تفاصيل الطلب"""
    from apps.audit.models import AuditLog
    
    req = get_object_or_404(Request, pk=pk, is_deleted=False)
    
    # المرفقات
    attachments = req.attachments.all()
    
    # سجل التدقيق للطلب (استخدام object_id بدلاً من request_id)
    audit_logs = AuditLog.objects.filter(
        object_id=str(req.id),
        model_name='request'
    ).select_related('user').order_by('-timestamp')[:20]
    
    # معلومات الدفع
    payment = None
    try:
        payment = req.payment
    except:
        pass
    
    context = {
        'page_title': f'تفاصيل الطلب {req.reference_number}',
        'request': req,
        'attachments': attachments,
        'audit_logs': audit_logs,
        'payment': payment,
    }
    return render(request, 'requests/detail.html', context)


# @login_required
def edit(request, pk):
    """تعديل طلب"""
    req = get_object_or_404(Request, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        # تحديث البيانات الأساسية
        req.description = request.POST.get('description', req.description)
        req.notes = request.POST.get('notes', req.notes)
        req.internal_notes = request.POST.get('internal_notes', req.internal_notes)
        req.priority = request.POST.get('priority', req.priority)
        req.status = request.POST.get('status', req.status)
        
        # تحديث المبلغ
        total_amount = request.POST.get('total_amount')
        if total_amount:
            req.total_amount = total_amount
        
        # تحديث تاريخ الاستحقاق
        due_date = request.POST.get('due_date')
        if due_date:
            req.due_date = due_date
        
        # تحديث المسند إلى
        assigned_to_id = request.POST.get('assigned_to')
        if assigned_to_id:
            from django.contrib.auth.models import User
            req.assigned_to = get_object_or_404(User, pk=assigned_to_id)
        else:
            req.assigned_to = None
        
        # تحديث نوع الطلب
        request_type_id = request.POST.get('request_type_id')
        if request_type_id:
            from apps.requests.models import RequestType
            req.request_type = get_object_or_404(RequestType, pk=request_type_id)
        
        # تحديث القالب
        template_id = request.POST.get('template_id')
        if template_id:
            req.template = get_object_or_404(Template, pk=template_id)
        
        req.save()
        
        # رفع مستند جديد (إذا وجد)
        if request.FILES.get('attachment'):
            from apps.core_utils.models import Attachment
            attachment = Attachment.objects.create(
                request=req,
                file=request.FILES['attachment'],
                description=request.POST.get('attachment_description', 'مستند مرفق'),
                uploaded_by=request.user if request.user.is_authenticated else None
            )
        
        messages.success(request, f'✅ تم تحديث الطلب {req.reference_number} بنجاح')
        return redirect('requests:detail', pk=req.pk)
    
    # GET request - عرض نموذج التعديل
    # جلب أنواع الطلبات
    from apps.requests.models import RequestType
    request_types = RequestType.objects.filter(is_active=True).select_related('category').order_by('category__display_order', 'display_order')
    
    # جلب القوالب
    templates = Template.objects.filter(is_active=True, is_published=True).order_by('template_type', 'name')
    
    # جلب المرفقات
    attachments = req.attachments.all()
    
    # جلب معلومات الدفع
    payment = None
    try:
        payment = req.payment
    except:
        pass
    
    # خيارات الحالة
    from apps.requests.models import RequestStatus
    status_choices = RequestStatus.choices
    
    # جلب المستخدمين للتخصيص
    from django.contrib.auth.models import User
    users = User.objects.filter(is_active=True).order_by('first_name', 'username')
    
    context = {
        'page_title': f'تعديل الطلب {req.reference_number}',
        'request': req,
        'request_types': request_types,
        'templates': templates,
        'attachments': attachments,
        'payment': payment,
        'status_choices': status_choices,
        'users': users,
    }
    return render(request, 'requests/edit.html', context)


# @login_required
def approve(request, pk):
    """الموافقة على طلب"""
    req = get_object_or_404(Request, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        req.status = 'approved'
        req.save()
        
        messages.success(request, f'✅ تمت الموافقة على الطلب {req.reference_number}')
        return redirect('requests:detail', pk=req.pk)
    
    return redirect('requests:detail', pk=req.pk)


# @login_required
def reject(request, pk):
    """رفض طلب"""
    req = get_object_or_404(Request, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        req.status = 'rejected'
        req.save()
        
        messages.warning(request, f'❌ تم رفض الطلب {req.reference_number}')
        return redirect('requests:detail', pk=req.pk)
    
    return redirect('requests:detail', pk=req.pk)


# @login_required
def export_pdf(request, pk):
    """تصدير الطلب كـ PDF"""
    req = get_object_or_404(Request, pk=pk, is_deleted=False)
    
    # TODO: تنفيذ تصدير PDF لاحقاً
    messages.info(request, 'جاري تصدير PDF...')
    return redirect('requests:detail', pk=req.pk)


# @login_required
def delete(request, pk):
    """حذف طلب (soft delete)"""
    req = get_object_or_404(Request, pk=pk, is_deleted=False)
    
    if request.method == 'POST':
        # Soft delete
        req.is_deleted = True
        req.deleted_at = datetime.now()
        req.deleted_by = request.user if request.user.is_authenticated else None
        req.save()
        
        # تسجيل في سجل التدقيق
        from apps.audit.models import AuditLog
        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='delete',
            model_name='request',
            object_id=str(req.id),
            object_repr=req.reference_number,
            description=f'تم حذف الطلب {req.reference_number}',
        )
        
        messages.success(request, f'✅ تم حذف الطلب {req.reference_number} بنجاح')
        return redirect('requests:list')
    
    # GET request - عرض صفحة تأكيد الحذف
    context = {
        'page_title': f'حذف الطلب {req.reference_number}',
        'request': req,
    }
    return render(request, 'requests/delete_confirm.html', context)


# @login_required
def pending(request):
    """الطلبات المعلقة"""
    from django.utils import timezone
    
    # الفلاتر
    priority_filter = request.GET.get('priority')
    duration_filter = request.GET.get('duration')
    
    # Query
    pending_requests = Request.objects.filter(
        status__in=['new', 'in_review', 'pending_payment'],
        is_deleted=False
    ).select_related('customer', 'created_by', 'assigned_to')
    
    if priority_filter and priority_filter != 'all':
        pending_requests = pending_requests.filter(priority=priority_filter)
    
    # فلتر المدة
    if duration_filter:
        now = timezone.now()
        if duration_filter == 'overdue':
            pending_requests = pending_requests.filter(due_date__lt=now)
        elif duration_filter == 'today':
            pending_requests = pending_requests.filter(created_at__date=date.today())
        elif duration_filter == 'week':
            week_ago = now - timezone.timedelta(days=7)
            pending_requests = pending_requests.filter(created_at__gte=week_ago)
    
    pending_requests = pending_requests.order_by('-priority', '-created_at')
    
    # Pagination
    paginator = Paginator(pending_requests, 15)  # 15 طلب لكل صفحة
    page = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # إحصائيات
    total_pending = Request.objects.filter(
        status__in=['new', 'in_review', 'pending_payment'],
        is_deleted=False
    ).count()
    overdue_count = Request.objects.filter(
        status__in=['new', 'in_review'],
        due_date__lt=timezone.now(),
        is_deleted=False
    ).count()
    
    # المخصصة للمستخدم الحالي
    assigned_to_me = 0
    if request.user.is_authenticated:
        assigned_to_me = Request.objects.filter(
            assigned_to=request.user,
            status__in=['new', 'in_review'],
            is_deleted=False
        ).count()
    
    context = {
        'page_title': 'الطلبات المعلقة',
        'page_obj': page_obj,
        'total_pending': total_pending,
        'overdue_count': overdue_count,
        'assigned_to_me': assigned_to_me,
    }
    return render(request, 'requests/pending.html', context)


# @login_required
def templates_list(request):
    """القوالب القانونية"""
    from django.db.models import Count
    
    # الفلاتر
    type_filter = request.GET.get('type')
    status_filter = request.GET.get('status')
    
    # Query - لا نستخدم annotate لأن usage_count موجود في Model
    templates = Template.objects.all()
    
    if type_filter and type_filter != 'all':
        templates = templates.filter(template_type=type_filter)
    
    if status_filter and status_filter != 'all':
        if status_filter == 'active':
            templates = templates.filter(is_active=True, is_published=True)
        elif status_filter == 'draft':
            templates = templates.filter(is_published=False)
        elif status_filter == 'archived':
            templates = templates.filter(is_active=False)
    
    templates = templates.order_by('-updated_at')
    
    # إحصائيات
    total_templates = Template.objects.count()
    active_templates = Template.objects.filter(is_active=True, is_published=True).count()
    draft_templates = Template.objects.filter(is_published=False).count()
    
    # إجمالي الاستخدامات من جميع القوالب
    total_usage = sum(t.usage_count for t in Template.objects.all())
    
    context = {
        'page_title': 'القوالب القانونية',
        'templates': templates,
        'total_templates': total_templates,
        'active_templates': active_templates,
        'draft_templates': draft_templates,
        'total_usage': total_usage,
    }
    return render(request, 'requests/templates_list.html', context)


# @login_required
def template_create(request):
    """إنشاء قالب قانوني جديد"""
    if request.method == 'POST':
        # جلب البيانات
        name = request.POST.get('name')
        name_english = request.POST.get('name_english', '')
        version = request.POST.get('version', '1.0')
        template_type = request.POST.get('template_type')
        content_arabic = request.POST.get('content_arabic')
        content_english = request.POST.get('content_english', '')
        
        # الحالات
        is_active = request.POST.get('is_active') == 'on'
        is_published = request.POST.get('is_published') == 'on'
        requires_admin_approval = request.POST.get('requires_admin_approval') == 'on'
        save_as_draft = request.POST.get('save_as_draft')
        
        # إنشاء القالب (الرمز سيُنشأ تلقائياً في save())
        template = Template.objects.create(
            name=name,
            name_english=name_english,
            # code will be auto-generated in save()
            version=version,
            template_type=template_type,
            content_arabic=content_arabic,
            content_english=content_english,
            is_active=is_active if not save_as_draft else False,
            is_published=is_published if not save_as_draft else False,
            requires_admin_approval=requires_admin_approval,
            created_by=request.user if request.user.is_authenticated else None
        )
        
        # رفع الملف (إذا وجد)
        if request.FILES.get('file'):
            template.file = request.FILES['file']
            template.save()
        
        # رسالة نجاح مع عرض الرمز المُنشأ تلقائياً
        if save_as_draft:
            messages.success(request, f'تم حفظ القالب "{template.name}" كمسودة بنجاح! الرمز: {template.code}')
        else:
            messages.success(request, f'تم إنشاء القالب "{template.name}" بنجاح! الرمز: {template.code}')
        
        return redirect('requests:templates_list')
    
    # GET request
    context = {
        'page_title': 'إضافة قالب جديد',
    }
    return render(request, 'requests/template_create.html', context)


# @login_required
def template_edit(request, pk):
    """تعديل قالب قانوني"""
    template = get_object_or_404(Template, pk=pk)
    
    if request.method == 'POST':
        # تحديث البيانات
        template.name = request.POST.get('name')
        template.name_english = request.POST.get('name_english', '')
        template.version = request.POST.get('version')
        template.template_type = request.POST.get('template_type')
        template.content_arabic = request.POST.get('content_arabic')
        template.content_english = request.POST.get('content_english', '')
        
        # الحالات
        template.is_active = request.POST.get('is_active') == 'on'
        template.is_published = request.POST.get('is_published') == 'on'
        template.requires_admin_approval = request.POST.get('requires_admin_approval') == 'on'
        
        # نشر مباشرة
        if request.POST.get('publish'):
            template.is_published = True
            template.is_active = True
        
        # رفع ملف جديد (إذا وجد)
        if request.FILES.get('file'):
            template.file = request.FILES['file']
        
        template.save()
        
        # رسالة نجاح
        messages.success(request, f'تم تحديث القالب "{template.name}" بنجاح!')
        return redirect('requests:templates_list')
    
    # GET request
    context = {
        'page_title': f'تعديل القالب: {template.name}',
        'template': template,
    }
    return render(request, 'requests/template_edit.html', context)


# @login_required
def request_types_list(request):
    """قائمة أنواع الطلبات"""
    from apps.requests.models import RequestType
    
    # جلب جميع الأنواع
    request_types = RequestType.objects.all().order_by('category', 'display_order')
    
    # إحصائيات
    total_types = RequestType.objects.count()
    active_types = RequestType.objects.filter(is_active=True).count()
    total_usage = sum(t.usage_count for t in RequestType.objects.all())
    
    context = {
        'page_title': 'إدارة أنواع الطلبات',
        'request_types': request_types,
        'total_types': total_types,
        'active_types': active_types,
        'total_usage': total_usage,
    }
    return render(request, 'requests/request_types_list.html', context)


# @login_required
def request_type_create(request):
    """إنشاء نوع طلب جديد"""
    from apps.requests.models import RequestType, RequestCategory
    
    if request.method == 'POST':
        name_arabic = request.POST.get('name_arabic')
        name_english = request.POST.get('name_english', '')
        category_id = request.POST.get('category_id')
        description = request.POST.get('description', '')
        default_price = request.POST.get('default_price', 420)
        display_order = request.POST.get('display_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        # جلب الفئة
        category = get_object_or_404(RequestCategory, pk=category_id) if category_id else None
        
        # إنشاء النوع (الرمز سيتم توليده تلقائياً)
        request_type = RequestType.objects.create(
            name_arabic=name_arabic,
            name_english=name_english,
            category=category,
            description=description,
            default_price=default_price,
            display_order=display_order,
            is_active=is_active,
            created_by=request.user if request.user.is_authenticated else None
        )
        
        messages.success(request, f'تم إنشاء نوع الطلب "{request_type.name_arabic}" بنجاح! الرمز: {request_type.code}')
        return redirect('requests:request_types_list')
    
    # GET - جلب الفئات
    categories = RequestCategory.objects.filter(is_active=True).order_by('display_order')
    
    context = {
        'page_title': 'إضافة نوع طلب جديد',
        'categories': categories,
    }
    return render(request, 'requests/request_type_create.html', context)


# @login_required
def request_type_edit(request, pk):
    """تعديل نوع طلب"""
    from apps.requests.models import RequestType
    request_type = get_object_or_404(RequestType, pk=pk)
    
    if request.method == 'POST':
        request_type.name_arabic = request.POST.get('name_arabic')
        request_type.name_english = request.POST.get('name_english', '')
        request_type.category = request.POST.get('category')
        request_type.description = request.POST.get('description', '')
        request_type.default_price = request.POST.get('default_price', 420)
        request_type.display_order = request.POST.get('display_order', 0)
        request_type.is_active = request.POST.get('is_active') == 'on'
        
        request_type.save()
        
        messages.success(request, f'تم تحديث نوع الطلب "{request_type.name_arabic}" بنجاح!')
        return redirect('requests:request_types_list')
    
    context = {
        'page_title': f'تعديل: {request_type.name_arabic}',
        'request_type': request_type,
    }
    return render(request, 'requests/request_type_edit.html', context)


# @login_required
def categories_list(request):
    """قائمة فئات الطلبات"""
    from apps.requests.models import RequestCategory
    
    categories = RequestCategory.objects.all().order_by('display_order', 'name_arabic')
    
    context = {
        'page_title': 'إدارة فئات الطلبات',
        'categories': categories,
    }
    return render(request, 'requests/categories_list.html', context)


# @login_required
def category_create(request):
    """إنشاء فئة جديدة"""
    from apps.requests.models import RequestCategory
    
    if request.method == 'POST':
        name_arabic = request.POST.get('name_arabic')
        name_english = request.POST.get('name_english', '')
        icon = request.POST.get('icon', 'fa-list')
        color = request.POST.get('color', 'primary')
        display_order = request.POST.get('display_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        # إنشاء الفئة (الرمز سيتم توليده تلقائياً)
        category = RequestCategory.objects.create(
            name_arabic=name_arabic,
            name_english=name_english,
            icon=icon,
            color=color,
            display_order=display_order,
            is_active=is_active
        )
        
        messages.success(request, f'تم إنشاء الفئة "{category.name_arabic}" بنجاح!')
        return redirect('requests:categories_list')
    
    context = {
        'page_title': 'إضافة فئة جديدة',
    }
    return render(request, 'requests/category_create.html', context)


# @login_required  
def category_edit(request, pk):
    """تعديل فئة"""
    from apps.requests.models import RequestCategory
    category = get_object_or_404(RequestCategory, pk=pk)
    
    if request.method == 'POST':
        category.name_arabic = request.POST.get('name_arabic')
        category.name_english = request.POST.get('name_english', '')
        category.icon = request.POST.get('icon', 'fa-list')
        category.color = request.POST.get('color', 'primary')
        category.display_order = request.POST.get('display_order', 0)
        category.is_active = request.POST.get('is_active') == 'on'
        
        category.save()
        
        messages.success(request, f'تم تحديث الفئة "{category.name_arabic}" بنجاح!')
        return redirect('requests:categories_list')
    
    context = {
        'page_title': f'تعديل: {category.name_arabic}',
        'category': category,
    }
    return render(request, 'requests/category_edit.html', context)
