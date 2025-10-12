from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import AuditLog
from datetime import date


# @login_required
def trail(request):
    """سجل التدقيق"""
    # الفلاتر
    action_filter = request.GET.get('action')
    user_filter = request.GET.get('user')
    model_filter = request.GET.get('model')
    
    # Query
    logs = AuditLog.objects.select_related('user')
    
    if action_filter:
        logs = logs.filter(action=action_filter)
    
    if user_filter:
        logs = logs.filter(user_id=user_filter)
    
    if model_filter:
        logs = logs.filter(model_name=model_filter)
    
    logs = logs.order_by('-timestamp')[:100]  # آخر 100 عملية
    
    # إحصائيات
    today_logs_count = AuditLog.objects.filter(timestamp__date=date.today()).count()
    active_users_count = User.objects.filter(is_active=True).count()
    critical_logs_count = AuditLog.objects.filter(severity='critical').count()
    
    context = {
        'page_title': 'سجل التدقيق',
        'logs': logs,
        'today_logs_count': today_logs_count,
        'active_users_count': active_users_count,
        'critical_logs_count': critical_logs_count,
    }
    return render(request, 'audit/trail.html', context)
