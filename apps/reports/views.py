from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Report
from apps.requests.models import Request
from apps.clients.models import Customer
from apps.payments.models import Payment
from django.db.models import Count, Sum
from datetime import datetime, timedelta


# @login_required
def dashboard(request):
    """لوحة التقارير"""
    # الفلاتر
    period = request.GET.get('period', 'month')  # week, month, year
    
    # حساب التواريخ
    today = datetime.now().date()
    if period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'year':
        start_date = today - timedelta(days=365)
    else:  # month
        start_date = today - timedelta(days=30)
    
    # إحصائيات الطلبات
    requests_stats = {
        'total': Request.objects.filter(is_deleted=False).count(),
        'new': Request.objects.filter(status='new', is_deleted=False).count(),
        'in_review': Request.objects.filter(status='in_review', is_deleted=False).count(),
        'completed': Request.objects.filter(status='completed', is_deleted=False).count(),
        'period_count': Request.objects.filter(
            created_at__date__gte=start_date,
            is_deleted=False
        ).count(),
    }
    
    # إحصائيات العملاء
    customers_stats = {
        'total': Customer.objects.filter(is_active=True).count(),
        'verified': Customer.objects.filter(is_verified=True).count(),
        'new_this_period': Customer.objects.filter(
            created_at__date__gte=start_date
        ).count(),
    }
    
    # إحصائيات المدفوعات
    payments_stats = {
        'total_paid': Payment.objects.filter(status='paid').aggregate(
            total=Sum('amount')
        )['total'] or 0,
        'pending_amount': Payment.objects.filter(status='pending').aggregate(
            total=Sum('amount')
        )['total'] or 0,
        'count': Payment.objects.count(),
    }
    
    # التقارير المحفوظة
    saved_reports = Report.objects.filter(status='completed').order_by('-generated_at')[:5]
    
    context = {
        'page_title': 'التقارير والإحصائيات',
        'requests_stats': requests_stats,
        'customers_stats': customers_stats,
        'payments_stats': payments_stats,
        'saved_reports': saved_reports,
        'period': period,
    }
    return render(request, 'reports/dashboard.html', context)
