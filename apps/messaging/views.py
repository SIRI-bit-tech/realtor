from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q, Count
from django.views.decorators.http import require_http_methods
from .models import Conversation, Message
from apps.properties.models import Property

User = get_user_model()


@login_required
def conversation_list(request):
    """List user's conversations"""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        message_count=Count('messages'),
        unread_count=Count('messages', filter=Q(messages__is_read=False, messages__sender__ne=request.user))
    ).prefetch_related('participants', 'messages')

    context = {
        'conversations': conversations,
    }

    return render(request, 'messaging/conversation_list.html', context)


@login_required
def conversation_detail(request, pk):
    """View conversation messages"""
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('messages__sender', 'participants'),
        pk=pk,
        participants=request.user
    )

    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

            if request.htmx:
                # Return the new message for HTMX
                message = conversation.messages.last()
                return render(request, 'partials/message_item.html', {
                    'message': message,
                    'user': request.user
                })

            return redirect('messaging:conversation_detail', pk=conversation.pk)

    context = {
        'conversation': conversation,
        'other_participant': conversation.get_other_participant(request.user),
    }

    return render(request, 'messaging/conversation_detail.html', context)


@login_required
@require_http_methods(["POST"])
def start_conversation(request):
    """Start a new conversation"""
    recipient_id = request.POST.get('recipient_id')
    property_id = request.POST.get('property_id')
    subject = request.POST.get('subject', 'Property Inquiry')
    content = request.POST.get('content', '').strip()

    if not recipient_id or not content:
        messages.error(request, 'Recipient and message content are required.')
        return redirect('core:home')

    try:
        recipient = User.objects.get(id=recipient_id)
        property_obj = None

        if property_id:
            property_obj = Property.objects.get(id=property_id)
            subject = f"Inquiry about {property_obj.title}"

        # Check if conversation already exists
        existing_conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=recipient
        ).filter(
            property=property_obj
        ).first()

        if existing_conversation:
            # Add message to existing conversation
            Message.objects.create(
                conversation=existing_conversation,
                sender=request.user,
                content=content
            )
            conversation = existing_conversation
        else:
            # Create new conversation
            conversation = Conversation.objects.create(
                subject=subject,
                property=property_obj
            )
            conversation.participants.add(request.user, recipient)

            # Add first message
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

        messages.success(request, 'Message sent successfully!')
        return redirect('messaging:conversation_detail', pk=conversation.pk)

    except (User.DoesNotExist, Property.DoesNotExist):
        messages.error(request, 'Invalid recipient or property.')
        return redirect('core:home')

