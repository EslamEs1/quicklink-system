from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone
from functools import wraps
from .models import UserProfile


def role_required(allowed_roles):
    """Decorator للتحقق من صلاحيات المستخدم"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            user_role = getattr(request.user.profile, 'role', None)
            if user_role not in allowed_roles:
                messages.error(request, 'ليس لديك صلاحية للوصول لهذه الصفحة')
                return redirect('requests:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def login(request):
    """تسجيل الدخول"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'مرحباً {user.get_full_name() or user.username}!')
            return redirect('requests:dashboard')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    
    context = {
        'page_title': 'تسجيل الدخول',
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    """تسجيل الخروج"""
    auth_logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('accounts:login')


@login_required
def profile(request):
    """الملف الشخصي"""
    if request.method == 'POST':
        # تحديث البيانات
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # تحديث Profile
        if hasattr(user, 'profile'):
            user.profile.phone = request.POST.get('phone', user.profile.phone)
            user.profile.save()
        
        messages.success(request, 'تم تحديث البيانات الشخصية بنجاح')
        return redirect('accounts:profile')
    
    context = {
        'page_title': 'الملف الشخصي',
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@role_required(['admin', 'manager'])
def users_list(request):
    """قائمة المستخدمين"""
    # الفلاتر
    role_filter = request.GET.get('role')
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')
    
    # Query
    users = User.objects.select_related('profile').all()
    
    if role_filter and role_filter != 'all':
        users = users.filter(profile__role=role_filter)
    
    if status_filter:
        if status_filter == 'active':
            users = users.filter(is_active=True, profile__is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(Q(is_active=False) | Q(profile__is_active=False))
        elif status_filter == 'suspended':
            users = users.filter(is_active=False)
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(profile__employee_id__icontains=search_query)
        )
    
    users = users.order_by('-date_joined')
    
    # إحصائيات
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    admin_users = UserProfile.objects.filter(role__in=['admin', 'manager']).count()
    
    # المتصلين الآن (آخر 15 دقيقة)
    fifteen_mins_ago = timezone.now() - timezone.timedelta(minutes=15)
    online_users = UserProfile.objects.filter(
        last_activity__gte=fifteen_mins_ago
    ).count()
    
    # إحصائيات الأدوار
    role_stats = UserProfile.objects.values('role').annotate(count=Count('id'))
    
    context = {
        'page_title': 'إدارة المستخدمين',
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users,
        'online_users': online_users,
        'role_stats': role_stats,
    }
    return render(request, 'accounts/users.html', context)


@login_required
@role_required(['admin'])
def permissions_manage(request):
    """إدارة الصلاحيات"""
    # جلب جميع المستخدمين مع صلاحياتهم
    users = User.objects.select_related('profile').filter(is_active=True)
    
    if request.method == 'POST':
        # حفظ الصلاحيات
        # TODO: تنفيذ منطق حفظ الصلاحيات
        messages.success(request, 'تم حفظ الصلاحيات بنجاح')
        return redirect('accounts:permissions')
    
    # إحصائيات الأدوار
    role_counts = UserProfile.objects.values('role').annotate(count=Count('id'))
    
    context = {
        'page_title': 'إدارة الصلاحيات',
        'users': users,
        'role_counts': role_counts,
    }
    return render(request, 'accounts/permissions.html', context)


@login_required
@role_required(['admin', 'manager'])
def create_user(request):
    """إنشاء مستخدم جديد"""
    if request.method == 'POST':
        try:
            # إنشاء المستخدم
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            # إنشاء User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # تحديث Profile
            if hasattr(user, 'profile'):
                user.profile.department = request.POST.get('department', 'غير محدد')
                user.profile.job_title = request.POST.get('job_title', 'غير محدد')
                user.profile.phone = request.POST.get('phone', 'غير محدد')
                user.profile.role = request.POST.get('role', 'intake')
                user.profile.save()
            
            messages.success(request, f'تم إنشاء المستخدم {user.get_full_name()} بنجاح')
            return redirect('accounts:users')
            
        except Exception as e:
            messages.error(request, f'خطأ في إنشاء المستخدم: {str(e)}')
    
    context = {
        'page_title': 'إنشاء مستخدم جديد',
    }
    return render(request, 'accounts/create_user.html', context)


@login_required
@role_required(['admin', 'manager'])
def edit_user(request, user_id):
    """تعديل مستخدم"""
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        try:
            # تحديث بيانات User
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.is_active = 'is_active' in request.POST
            
            # تحديث كلمة المرور إذا تم إدخالها
            new_password = request.POST.get('new_password')
            if new_password:
                user.set_password(new_password)
            
            user.save()
            
            # تحديث Profile
            if hasattr(user, 'profile'):
                user.profile.department = request.POST.get('department', user.profile.department)
                user.profile.job_title = request.POST.get('job_title', user.profile.job_title)
                user.profile.phone = request.POST.get('phone', user.profile.phone)
                user.profile.role = request.POST.get('role', user.profile.role)
                user.profile.is_active = user.is_active
                user.profile.save()
            
            messages.success(request, f'تم تحديث بيانات المستخدم {user.get_full_name()} بنجاح')
            return redirect('accounts:users')
            
        except Exception as e:
            messages.error(request, f'خطأ في تحديث المستخدم: {str(e)}')
    
    context = {
        'page_title': f'تعديل المستخدم: {user.get_full_name()}',
        'edit_user': user,
    }
    return render(request, 'accounts/edit_user.html', context)


@login_required
@role_required(['admin'])
def delete_user(request, user_id):
    """حذف مستخدم"""
    user = get_object_or_404(User, pk=user_id)
    
    # منع حذف المستخدم الحالي
    if user == request.user:
        messages.error(request, 'لا يمكنك حذف حسابك الخاص')
        return redirect('accounts:users')
    
    if request.method == 'POST':
        try:
            username = user.get_full_name() or user.username
            user.delete()
            messages.success(request, f'تم حذف المستخدم {username} بنجاح')
            return redirect('accounts:users')
        except Exception as e:
            messages.error(request, f'خطأ في حذف المستخدم: {str(e)}')
    
    context = {
        'page_title': f'حذف المستخدم: {user.get_full_name()}',
        'delete_user': user,
    }
    return render(request, 'accounts/delete_user.html', context)
