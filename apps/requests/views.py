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
        # التحقق من خيار العميل
        existing_customer_id = request.POST.get('existing_customer_id')
        
        if existing_customer_id:
            # استخدام عميل موجود
            customer = get_object_or_404(Customer, pk=existing_customer_id)
            customer_created = False
        else:
            # إنشاء عميل جديد
            full_name = request.POST.get('customerName')
            emirates_id = request.POST.get('emiratesId')
            phone = request.POST.get('phone')
            email = request.POST.get('email', '')
            date_of_birth = request.POST.get('dateOfBirth')
            gender = request.POST.get('gender', 'male')
            nationality = request.POST.get('nationality', 'الإمارات')
            
            # التحقق من عدم وجود نفس رقم الهوية
            if Customer.objects.filter(emirates_id=emirates_id).exists():
                messages.error(request, 'رقم الهوية موجود مسبقاً! استخدم "اختيار عميل موجود"')
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
            customer_created = True
        
        # إنشاء الطلب
        new_request = Request.objects.create(
            customer=customer,
            request_type=request.POST.get('requestType', 'paytabs_link'),
            priority='medium',
            total_amount=request.POST.get('amount', 420),
            description=request.POST.get('description', ''),
            created_by=request.user if request.user.is_authenticated else None,
        )
        
        # رسالة نجاح
        if customer_created:
            messages.success(request, f'تم إنشاء ملف العميل "{customer.full_name}" والطلب بنجاح! الرقم المرجعي: {new_request.reference_number}')
        else:
            messages.success(request, f'تم إنشاء الطلب بنجاح للعميل "{customer.full_name}"! الرقم المرجعي: {new_request.reference_number}')
        
        # إعادة التوجيه
        return redirect('requests:detail', pk=new_request.pk)
    
    # GET request - جلب قائمة العملاء للاختيار
    customers = Customer.objects.filter(is_active=True).order_by('-updated_at')[:50]
    templates = Template.objects.filter(is_active=True, is_published=True)
    
    # جلب أنواع الطلبات من Model
    request_types = Request.REQUEST_TYPE_CHOICES
    
    context = {
        'page_title': 'إنشاء طلب جديد',
        'templates': templates,
        'customers': customers,
        'request_types': request_types,  # أنواع الطلبات الديناميكية
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
    
    # سجل التدقيق للطلب
    audit_logs = AuditLog.objects.filter(
        request_id=req.id
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
        # تحديث البيانات
        req.description = request.POST.get('description', req.description)
        req.notes = request.POST.get('notes', req.notes)
        req.priority = request.POST.get('priority', req.priority)
        req.save()
        
        messages.success(request, 'تم تحديث الطلب بنجاح')
        return redirect('requests:detail', pk=req.pk)
    
    context = {
        'page_title': f'تعديل الطلب {req.reference_number}',
        'request': req,
    }
    return render(request, 'requests/edit.html', context)


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
    
    # Query
    templates = Template.objects.annotate(
        usage_count=Count('requests')
    )
    
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
    total_usage = Template.objects.aggregate(
        total=Count('requests')
    )['total'] or 0
    
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
        code = request.POST.get('code')
        version = request.POST.get('version', '1.0')
        template_type = request.POST.get('template_type')
        content_arabic = request.POST.get('content_arabic')
        content_english = request.POST.get('content_english', '')
        
        # الحالات
        is_active = request.POST.get('is_active') == 'on'
        is_published = request.POST.get('is_published') == 'on'
        requires_admin_approval = request.POST.get('requires_admin_approval') == 'on'
        save_as_draft = request.POST.get('save_as_draft')
        
        # التحقق من عدم تكرار الرمز
        if Template.objects.filter(code=code).exists():
            messages.error(request, f'رمز القالب "{code}" موجود مسبقاً! استخدم رمز آخر.')
            return redirect('requests:template_create')
        
        # إنشاء القالب
        template = Template.objects.create(
            name=name,
            name_english=name_english,
            code=code,
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
        
        # رسالة نجاح
        if save_as_draft:
            messages.success(request, f'تم حفظ القالب "{template.name}" كمسودة بنجاح!')
        else:
            messages.success(request, f'تم إنشاء القالب "{template.name}" بنجاح!')
        
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
