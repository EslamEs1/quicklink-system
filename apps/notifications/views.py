from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Notification, SmartAlert


# @login_required
def list(request):
    """قائمة الإشعارات"""
    # الفلاتر
    notification_type_filter = request.GET.get('type')
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    
    # إشعارات المستخدم
    if request.user.is_authenticated:
        notifications = request.user.notifications.select_related('request')
    else:
        notifications = Notification.objects.all()
    
    # تطبيق الفلاتر
    if notification_type_filter and notification_type_filter != 'all':
        notifications = notifications.filter(notification_type=notification_type_filter)
    
    if status_filter:
        if status_filter == 'unread':
            notifications = notifications.filter(is_read=False)
        elif status_filter == 'read':
            notifications = notifications.filter(is_read=True)
    
    if priority_filter and priority_filter != 'all':
        notifications = notifications.filter(priority=priority_filter)
    
    notifications = notifications.order_by('-created_at')[:100]
    
    # إحصائيات
    all_notifications = request.user.notifications if request.user.is_authenticated else Notification.objects.all()
    total_count = all_notifications.count()
    unread_count = all_notifications.filter(is_read=False).count()
    read_count = all_notifications.filter(is_read=True).count()
    high_priority_count = all_notifications.filter(priority__in=['high', 'critical']).count()
    
    # النسب المئوية حسب النوع
    from django.db.models import Count
    notifications_by_type = all_notifications.values('notification_type').annotate(count=Count('id'))
    
    type_percentages = {}
    for item in notifications_by_type:
        if total_count > 0:
            type_percentages[item['notification_type']] = round((item['count'] / total_count) * 100, 1)
    
    context = {
        'page_title': 'الإشعارات',
        'notifications': notifications,
        'total_count': total_count,
        'unread_count': unread_count,
        'read_count': read_count,
        'high_priority_count': high_priority_count,
        'type_percentages': type_percentages,
    }
    return render(request, 'notifications/list.html', context)


# @login_required
def smart_alerts(request):
    """التنبيهات الذكية"""
    if request.method == 'POST':
        # إنشاء تنبيه جديد
        name = request.POST.get('name')
        alert_type = request.POST.get('alert_type')
        frequency = request.POST.get('frequency')
        description = request.POST.get('description', '')
        
        SmartAlert.objects.create(
            name=name,
            alert_type=alert_type,
            frequency=frequency,
            description=description,
            condition='{}',  # سيتم تحديثه لاحقاً
            created_by=request.user if request.user.is_authenticated else None,
        )
        
        messages.success(request, 'تم إنشاء التنبيه بنجاح')
        return redirect('notifications:smart_alerts')
    
    # GET request
    alerts = SmartAlert.objects.select_related('created_by').order_by('-created_at')
    
    # إحصائيات
    active_alerts = alerts.filter(is_active=True).count()
    inactive_alerts = alerts.filter(is_active=False).count()
    
    # عدد الإرسال اليوم
    from datetime import date
    today_executions = alerts.filter(last_run__date=date.today()).aggregate(
        total=models.Sum('execution_count')
    )['total'] or 0
    
    # إجمالي الإرسال
    total_executions = alerts.aggregate(total=models.Sum('execution_count'))['total'] or 0
    
    context = {
        'page_title': 'التنبيهات الذكية',
        'alerts': alerts,
        'active_alerts': active_alerts,
        'inactive_alerts': inactive_alerts,
        'today_executions': today_executions,
        'total_executions': total_executions,
    }
    return render(request, 'notifications/smart_alerts.html', context)
