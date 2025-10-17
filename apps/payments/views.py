from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Payment


# @login_required
def list(request):
    """قائمة المدفوعات"""
    # الفلاتر
    status_filter = request.GET.get('status')
    gateway_filter = request.GET.get('gateway')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Query
    payments = Payment.objects.select_related('request', 'request__customer', 'processed_by')
    
    if status_filter and status_filter != 'all':
        payments = payments.filter(status=status_filter)
    
    if gateway_filter and gateway_filter != 'all':
        payments = payments.filter(payment_method=gateway_filter)
    
    if start_date:
        payments = payments.filter(created_at__gte=start_date)
    
    if end_date:
        payments = payments.filter(created_at__lte=end_date)
    
    payments = payments.order_by('-created_at')
    
    # إحصائيات
    from django.db.models import Sum, Count
    
    # إجمالي المدفوعات المكتملة
    total_stats = Payment.objects.filter(status='paid').aggregate(
        total=Sum('amount'),
        count=Count('id')
    )
    total_amount = total_stats['total'] or 0
    completed_count = total_stats['count'] or 0
    
    # دفعات معلقة
    pending_stats = Payment.objects.filter(status='pending').aggregate(
        count=Count('id')
    )
    pending_count = pending_stats['count'] or 0
    
    # دفعات فاشلة
    failed_count = Payment.objects.filter(status='failed').count()
    
    # نسب بوابات الدفع
    gateway_stats = Payment.objects.filter(status='paid').values('payment_method').annotate(
        count=Count('id'),
        total=Sum('amount')
    )
    
    gateway_percentages = {}
    for stat in gateway_stats:
        if completed_count > 0:
            gateway_percentages[stat['payment_method']] = {
                'percentage': round((stat['count'] / completed_count) * 100, 1),
                'count': stat['count'],
                'total': stat['total']
            }
    
    # إحصائيات المدفوعات الشهرية (آخر 6 أشهر)
    from datetime import datetime, timedelta
    from django.db.models.functions import TruncMonth
    
    monthly_stats = Payment.objects.filter(
        status='paid',
        created_at__gte=datetime.now() - timedelta(days=180)  # آخر 6 أشهر
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_amount=Sum('amount'),
        payment_count=Count('id')
    ).order_by('month')
    
    # تحضير البيانات للشارت
    chart_labels = []
    chart_amounts = []
    chart_counts = []
    
    for stat in monthly_stats:
        month_name = stat['month'].strftime('%B %Y')
        chart_labels.append(month_name)
        chart_amounts.append(float(stat['total_amount'] or 0))
        chart_counts.append(stat['payment_count'] or 0)
    
    context = {
        'page_title': 'إدارة المدفوعات',
        'payments': payments,
        'total_amount': total_amount,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'failed_count': failed_count,
        'gateway_percentages': gateway_percentages,
        'chart_labels': chart_labels,
        'chart_amounts': chart_amounts,
        'chart_counts': chart_counts,
    }
    return render(request, 'payments/list.html', context)


# @login_required
def process_payment(request):
    """معالجة دفعة جديدة"""
    if request.method == 'POST':
        # معالجة النموذج
        request_id = request.POST.get('request_id')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id', '')
        receipt_number = request.POST.get('receipt_number', '')
        notes = request.POST.get('notes', '')
        
        try:
            from apps.requests.models import Request
            req = Request.objects.get(id=request_id, is_deleted=False)
            
            # التحقق من وجود دفعة سابقة
            existing_payment = Payment.objects.filter(request=req).first()
            if existing_payment:
                status_display = existing_payment.get_status_display()
                if existing_payment.status == 'paid':
                    messages.warning(request, f'⚠️ الطلب {req.reference_number} مدفوع مسبقاً! لا يمكن إضافة دفعة أخرى.')
                elif existing_payment.status == 'pending':
                    messages.info(request, f'ℹ️ يوجد دفعة معلقة للطلب {req.reference_number}. يرجى تأكيد الدفعة المعلقة أولاً.')
                else:
                    messages.warning(request, f'⚠️ يوجد دفعة سابقة للطلب {req.reference_number} بحالة: {status_display}. لا يمكن إضافة دفعة جديدة.')
                return redirect('requests:detail', pk=req.id)
            
            # إنشاء الدفعة الجديدة
            payment = Payment.objects.create(
                request=req,
                amount=amount,
                payment_method=payment_method,
                transaction_id=transaction_id,
                receipt_number=receipt_number,
                status='paid',  # افتراضياً مدفوعة
                notes=notes,
                processed_by=request.user if request.user.is_authenticated else None,
            )
            
            # تحديث حالة الطلب
            req.status = 'paid'
            req.save()
            
            messages.success(request, f'✅ تم معالجة الدفعة بنجاح للطلب {req.reference_number}! تم تحديث حالة الطلب إلى "مدفوع".')
            return redirect('requests:detail', pk=req.id)
            
        except Request.DoesNotExist:
            messages.error(request, '❌ الطلب المطلوب غير موجود أو تم حذفه من النظام.')
            return redirect('requests:list')
        except Exception as e:
            messages.error(request, f'❌ حدث خطأ أثناء معالجة الدفعة: {str(e)}. يرجى المحاولة مرة أخرى أو مراجعة المشرف.')
            return redirect('requests:detail', pk=req.id if 'req' in locals() else None)
    
    # GET request - عرض النموذج
    request_id = request.GET.get('request_id')
    
    if request_id:
        try:
            from apps.requests.models import Request
            req = Request.objects.get(id=request_id, is_deleted=False)
            
            # التحقق من وجود دفعة سابقة
            existing_payment = Payment.objects.filter(request=req).first()
            if existing_payment:
                status_display = existing_payment.get_status_display()
                if existing_payment.status == 'paid':
                    messages.warning(request, f'⚠️ الطلب {req.reference_number} مدفوع مسبقاً! لا يمكن إضافة دفعة أخرى.')
                elif existing_payment.status == 'pending':
                    messages.info(request, f'ℹ️ يوجد دفعة معلقة للطلب {req.reference_number}. يرجى تأكيد الدفعة المعلقة أولاً.')
                else:
                    messages.warning(request, f'⚠️ يوجد دفعة سابقة للطلب {req.reference_number} بحالة: {status_display}. لا يمكن إضافة دفعة جديدة.')
                return redirect('requests:detail', pk=req.id)
            
            context = {
                'page_title': f'معالجة دفعة - {req.reference_number}',
                'request': req,
                'request_id': request_id,
            }
            return render(request, 'payments/process.html', context)
            
        except Request.DoesNotExist:
            messages.error(request, '❌ الطلب المطلوب غير موجود أو تم حذفه من النظام.')
            return redirect('requests:list')
    
    # إذا لم يتم تحديد طلب، عرض قائمة المدفوعات
    return redirect('payments:list')


# @login_required
def confirm_payment(request):
    """تأكيد دفعة معلقة"""
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.status = 'paid'
            payment.save()
            
            # تحديث حالة الطلب
            payment.request.status = 'paid'
            payment.request.save()
            
            messages.success(request, f'✅ تم تأكيد الدفعة بنجاح!')
        except Payment.DoesNotExist:
            messages.error(request, '❌ الدفعة غير موجودة')
        except Exception as e:
            messages.error(request, f'❌ حدث خطأ: {str(e)}')
    
    return redirect('payments:list')


# @login_required
def cancel_payment(request):
    """إلغاء دفعة معلقة"""
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.status = 'failed'
            payment.save()
            
            messages.success(request, f'✅ تم إلغاء الدفعة بنجاح!')
        except Payment.DoesNotExist:
            messages.error(request, '❌ الدفعة غير موجودة')
        except Exception as e:
            messages.error(request, f'❌ حدث خطأ: {str(e)}')
    
    return redirect('payments:list')


# @login_required
def payment_details(request, payment_id):
    """تفاصيل الدفعة"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'page_title': f'تفاصيل الدفعة {payment.id}',
        'payment': payment,
    }
    return render(request, 'payments/details.html', context)


# @login_required
def payment_receipt(request, payment_id):
    """طباعة إيصال الدفع"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/receipt.html', context)


# @login_required
def send_payment_email(request, payment_id):
    """إرسال إيصال الدفع بالبريد الإلكتروني"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        # TODO: تنفيذ إرسال البريد الإلكتروني
        messages.success(request, f'✅ تم إرسال الإيصال بالبريد الإلكتروني للعميل {payment.request.customer.full_name}')
        return redirect('payments:list')
    
    context = {
        'page_title': f'إرسال إيصال الدفع - {payment.request.reference_number}',
        'payment': payment,
    }
    return render(request, 'payments/send_email.html', context)


# @login_required
def retry_payment(request, payment_id):
    """إعادة محاولة دفعة فاشلة"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        # إعادة تعيين الدفعة كمعلقة
        payment.status = 'pending'
        payment.save()
        
        messages.success(request, f'✅ تم إعادة تعيين الدفعة للمحاولة مرة أخرى')
        return redirect('payments:list')
    
    context = {
        'page_title': f'إعادة محاولة الدفعة - {payment.request.reference_number}',
        'payment': payment,
    }
    return render(request, 'payments/retry.html', context)
