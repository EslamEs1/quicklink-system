from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import SystemSetting


# @login_required
def general(request):
    """الإعدادات العامة"""
    if request.method == 'POST':
        # حفظ الإعدادات
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                SystemSetting.objects.update_or_create(
                    key=key,
                    defaults={
                        'value': value,
                        'updated_by': request.user if request.user.is_authenticated else None,
                    }
                )
        
        messages.success(request, 'تم حفظ الإعدادات بنجاح')
        return redirect('settings_app:general')
    
    # GET request
    settings = SystemSetting.objects.all()
    
    context = {
        'page_title': 'الإعدادات العامة',
        'settings': settings,
    }
    return render(request, 'settings/general.html', context)


# @login_required
def users(request):
    """إدارة المستخدمين"""
    # قائمة المستخدمين
    users_list = User.objects.select_related('profile').filter(is_active=True)
    
    # إحصائيات
    total_users = users_list.count()
    admins = users_list.filter(profile__role='admin').count()
    managers = users_list.filter(profile__role='manager').count()
    
    context = {
        'page_title': 'إدارة المستخدمين',
        'users': users_list,
        'total_users': total_users,
        'admins_count': admins,
        'managers_count': managers,
    }
    return render(request, 'settings/users.html', context)


# @login_required
def permissions(request):
    """إدارة الصلاحيات"""
    if request.method == 'POST':
        # تحديث الصلاحيات
        user_id = request.POST.get('user_id')
        # هنا سنضيف منطق الصلاحيات لاحقاً
        
        messages.success(request, 'تم تحديث الصلاحيات بنجاح')
        return redirect('settings_app:permissions')
    
    # GET request
    users_list = User.objects.select_related('profile').filter(is_active=True)
    
    context = {
        'page_title': 'إدارة الصلاحيات',
        'users': users_list,
    }
    return render(request, 'settings/permissions.html', context)
