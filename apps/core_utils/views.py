from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Attachment, Backup


# @login_required
def backup(request):
    """إدارة النسخ الاحتياطي"""
    if request.method == 'POST':
        # إنشاء نسخة احتياطية يدوية
        from datetime import datetime
        
        backup = Backup.objects.create(
            name=f"Backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            file_path=f"/backups/manual_{datetime.now().strftime('%Y%m%d%H%M%S')}.sql",
            file_size=0,  # سيتم تحديثه
            backup_type='manual',
            storage_location='local',
            created_by=request.user if request.user.is_authenticated else None,
        )
        
        messages.success(request, 'جاري إنشاء النسخة الاحتياطية...')
        return redirect('core_utils:backup')
    
    # GET request - الفلاتر
    storage_filter = request.GET.get('storage', 'all')
    
    backups = Backup.objects.select_related('created_by')
    
    if storage_filter == 'cloud':
        backups = backups.filter(storage_location__in=['aws_s3', 'google_drive'])
    elif storage_filter == 'local':
        backups = backups.filter(storage_location='local')
    
    backups = backups.order_by('-created_at')[:30]
    
    # إحصائيات
    local_backups_count = Backup.objects.filter(storage_location='local').count()
    cloud_backups_count = Backup.objects.filter(storage_location__in=['aws_s3', 'google_drive']).count()
    successful_backups_count = Backup.objects.filter(status='completed').count()
    failed_backups_count = Backup.objects.filter(status='failed').count()
    
    # آخر نسخة ناجحة
    last_backup = Backup.objects.filter(status='completed').order_by('-completed_at').first()
    
    context = {
        'page_title': 'النسخ الاحتياطي',
        'backups': backups,
        'local_backups_count': local_backups_count,
        'cloud_backups_count': cloud_backups_count,
        'successful_backups_count': successful_backups_count,
        'failed_backups_count': failed_backups_count,
        'last_backup': last_backup,
    }
    return render(request, 'core/backup.html', context)


# @login_required
def attachments(request, request_id=None):
    """إدارة المرفقات"""
    # الفلاتر
    category_filter = request.GET.get('category')
    
    # Query
    attachments_list = Attachment.objects.select_related('request', 'uploaded_by', 'approved_by')
    
    # إذا كان هناك request_id محدد
    if request_id:
        attachments_list = attachments_list.filter(request_id=request_id)
        from apps.requests.models import Request
        request_obj = Request.objects.filter(pk=request_id).first()
    else:
        request_obj = None
    
    if category_filter and category_filter != 'all':
        attachments_list = attachments_list.filter(category=category_filter)
    
    attachments_list = attachments_list.order_by('-uploaded_at')[:50]
    
    # إحصائيات
    total_files = attachments_list.count()
    image_files = attachments_list.filter(file_type__in=['image/jpeg', 'image/png', 'image/jpg']).count()
    pdf_files = attachments_list.filter(file_type='application/pdf').count()
    
    # حجم إجمالي (MB)
    from django.db.models import Sum
    total_size_bytes = attachments_list.aggregate(Sum('file_size'))['file_size__sum'] or 0
    total_size_mb = round(total_size_bytes / (1024 * 1024), 2)
    
    context = {
        'page_title': 'إدارة المرفقات',
        'attachments': attachments_list,
        'request_obj': request_obj,
        'total_files': total_files,
        'image_files': image_files,
        'pdf_files': pdf_files,
        'total_size_mb': total_size_mb,
    }
    return render(request, 'core/attachments.html', context)


def error(request):
    """صفحة الأخطاء"""
    error_code = request.GET.get('code', '404')
    error_message = request.GET.get('message', 'الصفحة غير موجودة')
    
    context = {
        'page_title': 'خطأ',
        'error_code': error_code,
        'error_message': error_message,
    }
    return render(request, 'core/error.html', context)


def help(request):
    """صفحة المساعدة"""
    context = {
        'page_title': 'المساعدة',
    }
    return render(request, 'core/help.html', context)


def privacy(request):
    """سياسة الخصوصية"""
    context = {
        'page_title': 'سياسة الخصوصية',
    }
    return render(request, 'core/privacy.html', context)


def terms(request):
    """الشروط والأحكام"""
    context = {
        'page_title': 'الشروط والأحكام',
    }
    return render(request, 'core/terms.html', context)


def run(request):
    """التشغيل السريع"""
    context = {
        'page_title': 'التشغيل السريع',
    }
    return render(request, 'core/run.html', context)
