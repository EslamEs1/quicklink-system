from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from datetime import date, timedelta
from .models import Customer, IdentityConflict


# @login_required
def list(request):
    """قائمة العملاء"""
    # الفلاتر
    search_query = request.GET.get('q')
    nationality_filter = request.GET.get('nationality')
    requests_filter = request.GET.get('requests')
    
    # Query
    customers = Customer.objects.filter(is_active=True).annotate(
        requests_count=Count('requests')
    )
    
    if search_query:
        customers = customers.filter(
            Q(full_name__icontains=search_query) |
            Q(emirates_id__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    if nationality_filter and nationality_filter != 'all':
        customers = customers.filter(nationality__icontains=nationality_filter)
    
    if requests_filter and requests_filter != 'all':
        if requests_filter == 'new':
            customers = customers.filter(requests_count__lte=1)
        elif requests_filter == 'regular':
            customers = customers.filter(requests_count__gte=2, requests_count__lte=5)
        elif requests_filter == 'vip':
            customers = customers.filter(requests_count__gt=5)
    
    customers = customers.order_by('-created_at')
    
    # إحصائيات
    total_customers = Customer.objects.filter(is_active=True).count()
    
    # عملاء جدد هذا الشهر
    first_day_of_month = date.today().replace(day=1)
    new_customers_count = Customer.objects.filter(
        is_active=True,
        created_at__gte=first_day_of_month
    ).count()
    
    # عملاء VIP (أكثر من 5 طلبات)
    vip_customers_count = Customer.objects.filter(is_active=True).annotate(
        requests_count=Count('requests')
    ).filter(requests_count__gt=5).count()
    
    # عملاء لديهم عيد ميلاد اليوم
    today = date.today()
    birthday_customers_count = Customer.objects.filter(
        is_active=True,
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    ).count()
    
    context = {
        'page_title': 'قاعدة العملاء',
        'customers': customers,
        'total_customers': total_customers,
        'new_customers_count': new_customers_count,
        'vip_customers_count': vip_customers_count,
        'birthday_customers_count': birthday_customers_count,
    }
    return render(request, 'clients/list.html', context)


# @login_required
def detail(request, pk):
    """تفاصيل العميل"""
    customer = get_object_or_404(Customer, pk=pk)
    
    # طلبات العميل
    customer_requests = customer.requests.filter(is_deleted=False).order_by('-created_at')
    
    # إحصائيات الطلبات
    total_requests = customer_requests.count()
    completed_requests = customer_requests.filter(status='completed').count()
    pending_requests = customer_requests.filter(status__in=['pending', 'review']).count()
    cancelled_requests = customer_requests.filter(status='cancelled').count()
    
    # التحقق من عيد الميلاد القريب
    today = date.today()
    days_until_birthday = None
    is_birthday_soon = False
    
    # حساب الأيام حتى عيد الميلاد القادم
    this_year_birthday = customer.date_of_birth.replace(year=today.year)
    if this_year_birthday < today:
        next_birthday = customer.date_of_birth.replace(year=today.year + 1)
    else:
        next_birthday = this_year_birthday
    
    days_until_birthday = (next_birthday - today).days
    is_birthday_soon = days_until_birthday <= 7  # أقل من 7 أيام
    
    context = {
        'page_title': f'ملف العميل: {customer.full_name}',
        'customer': customer,
        'requests': customer_requests,
        'total_requests': total_requests,
        'completed_requests': completed_requests,
        'pending_requests': pending_requests,
        'cancelled_requests': cancelled_requests,
        'days_until_birthday': days_until_birthday,
        'is_birthday_soon': is_birthday_soon,
    }
    return render(request, 'clients/detail.html', context)


# @login_required
def identity_check(request):
    """كشف التعارضات"""
    # الفلاتر
    status_filter = request.GET.get('status', 'active')
    search_name = request.GET.get('name')
    
    # Query
    conflicts = IdentityConflict.objects.select_related(
        'customer1', 'customer2'
    ).annotate(
        customer1_requests_count=Count('customer1__requests'),
        customer2_requests_count=Count('customer2__requests')
    )
    
    # تطبيق الفلاتر
    if status_filter == 'active':
        conflicts = conflicts.filter(status='pending')
    elif status_filter == 'review':
        conflicts = conflicts.filter(status='reviewing')
    elif status_filter == 'resolved':
        conflicts = conflicts.filter(status='resolved')
    elif status_filter != 'all':
        conflicts = conflicts.filter(status='pending')
    
    if search_name:
        conflicts = conflicts.filter(
            Q(customer1__full_name__icontains=search_name) |
            Q(customer2__full_name__icontains=search_name)
        )
    
    conflicts = conflicts.order_by('-detected_at')
    
    # إحصائيات
    active_conflicts = IdentityConflict.objects.filter(status='pending').count()
    reviewing_conflicts = IdentityConflict.objects.filter(status='reviewing').count()
    resolved_conflicts = IdentityConflict.objects.filter(status='resolved').count()
    
    context = {
        'page_title': 'كشف التعارضات',
        'conflicts': conflicts,
        'active_conflicts': active_conflicts,
        'reviewing_conflicts': reviewing_conflicts,
        'resolved_conflicts': resolved_conflicts,
    }
    return render(request, 'clients/identity_check.html', context)


# @login_required
def edit(request, pk):
    """تعديل بيانات العميل"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        # تحديث البيانات
        customer.full_name = request.POST.get('full_name')
        customer.full_name_english = request.POST.get('full_name_english', '')
        # رقم الهوية لا يتغير لأسباب أمنية
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email', '')
        customer.date_of_birth = request.POST.get('date_of_birth')
        customer.gender = request.POST.get('gender')
        customer.nationality = request.POST.get('nationality')
        customer.occupation = request.POST.get('occupation', '')
        customer.company_name = request.POST.get('company_name', '')
        customer.address = request.POST.get('address', '')
        customer.notes = request.POST.get('notes', '')
        customer.is_active = request.POST.get('is_active') == 'on'
        customer.is_verified = request.POST.get('is_verified') == 'on'
        
        customer.save()
        
        messages.success(request, 'تم تحديث بيانات العميل بنجاح!')
        return redirect('clients:detail', pk=customer.pk)
    
    # GET request
    context = {
        'page_title': f'تعديل بيانات: {customer.full_name}',
        'customer': customer,
    }
    return render(request, 'clients/edit.html', context)


# @login_required
def delete(request, pk):
    """حذف عميل نهائي"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer_name = customer.full_name
        
        # التحقق من وجود طلبات نشطة مرتبطة بالعميل (غير محذوفة)
        active_requests_count = customer.requests.filter(is_deleted=False).count()
        if active_requests_count > 0:
            messages.error(request, f'❌ لا يمكن حذف العميل "{customer_name}" لأنه لديه {active_requests_count} طلب(ات) نشط(ة). يرجى حذف الطلبات أولاً أو استخدام التعديل بدلاً من الحذف.')
            return redirect('clients:detail', pk=pk)
        
        # حذف نهائي للطلبات المحذوفة (soft deleted) أولاً لتجنب ProtectedError
        deleted_requests = customer.requests.filter(is_deleted=True)
        if deleted_requests.exists():
            # حذف المدفوعات والمرفقات المرتبطة بالطلبات المحذوفة أولاً
            from apps.payments.models import Payment
            from apps.core_utils.models import Attachment
            
            deleted_count = 0
            payments_deleted = 0
            attachments_deleted = 0
            
            for deleted_request in deleted_requests:
                # حذف المدفوعات المرتبطة بالطلب
                payments = Payment.objects.filter(request=deleted_request)
                if payments.exists():
                    payments_deleted += payments.count()
                    payments.delete()
                    print(f"✅ Deleted {payments.count()} payment(s) for request {deleted_request.reference_number}")
                
                # حذف المرفقات المرتبطة بالطلب
                attachments = Attachment.objects.filter(request=deleted_request)
                if attachments.exists():
                    attachments_deleted += attachments.count()
                    attachments.delete()
                    print(f"✅ Deleted {attachments.count()} attachment(s) for request {deleted_request.reference_number}")
                
                deleted_count += 1
            
            # حذف نهائي للطلبات المحذوفة
            deleted_requests.delete()
            
            # رسالة مفصلة عن ما تم حذفه
            cleanup_message = f'تم حذف {deleted_count} طلب محذوف نهائياً'
            if payments_deleted > 0:
                cleanup_message += f' مع {payments_deleted} دفعة'
            if attachments_deleted > 0:
                cleanup_message += f' و {attachments_deleted} مرفق'
            cleanup_message += '.'
            
            messages.info(request, cleanup_message)
        
        # حذف نهائي للعميل
        customer.delete()
        
        messages.success(request, f'✅ تم حذف العميل "{customer_name}" نهائياً من النظام')
        return redirect('clients:list')
    
    # GET request - عرض صفحة تأكيد الحذف
    # التحقق من الطلبات النشطة فقط (غير محذوفة)
    requests_count = customer.requests.filter(is_deleted=False).count()
    context = {
        'page_title': f'حذف العميل: {customer.full_name}',
        'customer': customer,
        'requests_count': requests_count,
    }
    return render(request, 'clients/delete_confirm.html', context)


# @login_required
def export_customer(request, pk):
    """تصدير بيانات العميل"""
    customer = get_object_or_404(Customer, pk=pk)
    # TODO: تنفيذ تصدير البيانات لاحقاً
    messages.info(request, 'جاري تصدير بيانات العميل...')
    return redirect('clients:detail', pk=pk)


# @login_required
def export_conflicts(request):
    """تصدير تقرير التعارضات"""
    # TODO: تنفيذ تصدير التقرير لاحقاً
    messages.info(request, 'جاري تصدير تقرير التعارضات...')
    return redirect('clients:identity_check')


# @login_required
def resolve_conflict(request, pk):
    """حل تعارض"""
    conflict = get_object_or_404(IdentityConflict, pk=pk)
    
    if request.method == 'POST':
        conflict.status = 'resolved'
        conflict.resolved_at = date.today()
        conflict.resolved_by = request.user if request.user.is_authenticated else None
        conflict.save()
        
        messages.success(request, 'تم حل التعارض بنجاح!')
        return redirect('clients:identity_check')
    
    return redirect('clients:identity_check')


# @login_required
def conflict_detail(request, pk):
    """تفاصيل التعارض"""
    conflict = get_object_or_404(IdentityConflict, pk=pk)
    
    context = {
        'page_title': 'تفاصيل التعارض',
        'conflict': conflict,
    }
    return render(request, 'clients/conflict_detail.html', context)


# @login_required
def add(request):
    """إضافة عميل جديد"""
    if request.method == 'POST':
        try:
            # إنشاء عميل جديد
            customer = Customer.objects.create(
                full_name=request.POST.get('full_name'),
                full_name_english=request.POST.get('full_name_english', ''),
                emirates_id=request.POST.get('emirates_id'),
                date_of_birth=request.POST.get('date_of_birth'),
                nationality=request.POST.get('nationality'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email', ''),
                address=request.POST.get('address', ''),
                occupation=request.POST.get('occupation', ''),
                company_name=request.POST.get('company_name', ''),
                notes=request.POST.get('notes', ''),
                is_verified=request.POST.get('is_verified') == 'on',
                is_active=request.POST.get('is_active') == 'on',
                created_by=request.user if request.user.is_authenticated else None
            )
            
            messages.success(request, f'تم إنشاء العميل {customer.full_name} بنجاح!')
            return redirect('clients:detail', pk=customer.id)
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء إنشاء العميل: {str(e)}')
    
    # إحصائيات للعرض في الـ sidebar
    total_customers = Customer.objects.filter(is_active=True).count()
    new_customers_count = Customer.objects.filter(
        is_active=True,
        created_at__gte=date.today() - timedelta(days=30)
    ).count()
    
    context = {
        'page_title': 'إضافة عميل جديد',
        'total_customers': total_customers,
        'new_customers_count': new_customers_count,
    }
    
    return render(request, 'clients/add.html', context)
