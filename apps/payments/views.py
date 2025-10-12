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
    
    context = {
        'page_title': 'إدارة المدفوعات',
        'payments': payments,
        'total_amount': total_amount,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'failed_count': failed_count,
        'gateway_percentages': gateway_percentages,
    }
    return render(request, 'payments/list.html', context)
