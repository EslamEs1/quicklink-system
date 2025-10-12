from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q, Count
from .models import ChatMessage
from apps.clients.models import Customer


# @login_required
def room(request):
    """صفحة المحادثات"""
    # العملاء الذين لديهم محادثات - مرتبين حسب آخر رسالة
    customers_with_chats = Customer.objects.filter(
        messages__isnull=False
    ).annotate(
        last_message_time=Max('messages__sent_at'),
        unread_count=Count('messages', filter=Q(messages__is_read=False, messages__direction='incoming'))
    ).distinct().order_by('-last_message_time')[:50]
    
    # إذا كان هناك customer_id في GET أو اختيار أول عميل
    customer_id = request.GET.get('customer_id')
    selected_customer = None
    messages_list = []
    
    if customer_id:
        selected_customer = get_object_or_404(Customer, pk=customer_id)
        messages_list = selected_customer.messages.select_related('sent_by').order_by('sent_at')
        
        # تحديد جميع الرسائل الواردة كمقروءة
        selected_customer.messages.filter(
            direction='incoming', 
            is_read=False
        ).update(is_read=True)
    elif customers_with_chats.exists():
        # اختيار أول محادثة بشكل افتراضي
        selected_customer = customers_with_chats.first()
        messages_list = selected_customer.messages.select_related('sent_by').order_by('sent_at')
    
    context = {
        'page_title': 'محادثات WhatsApp',
        'customers': customers_with_chats,
        'selected_customer': selected_customer,
        'messages': messages_list,
    }
    return render(request, 'chat/room.html', context)
