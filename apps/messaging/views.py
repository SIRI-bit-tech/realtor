from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Q, Count, Max
from django.core.paginator import Paginator
from .models import Conversation, Message
from apps.properties.models import Property
from apps.users.models import User

@login_required
def conversation_list(request):
    """Display list of user's conversations"""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        last_message_time=Max('messages__created_at'),
        unread_count=Count(
            'messages',
            filter=~Q(messages__sender=request.user) & Q(messages__is_read=False)
        )
    ).order_by('-last_message_time')
    
    # Add other_user and last_message to each conversation
    for conversation in conversations:
        conversation.other_user = conversation.get_other_participant(request.user)
        conversation.last_message = conversation.messages.order_by('-created_at').first()
    
    # Calculate total unread count
    unread_count = sum(conv.unread_count for conv in conversations)
    
    context = {
        'conversations': conversations,
        'unread_count': unread_count,
    }
    return render(request, 'messaging/conversation_list.html', context)

@login_required
def conversation_detail(request, conversation_id):
    """Display conversation detail with messages"""
    conversation = get_object_or_404(
        Conversation.objects.filter(
            participants=request.user
        ),
        id=conversation_id
    )
    # Get messages for this conversation
    messages_list = conversation.messages.select_related('sender').order_by('created_at')
    
    # Mark messages as read
    conversation.messages.filter(
        ~Q(sender=request.user),
        is_read=False
    ).update(is_read=True)
    
    # Determine other user
    conversation.other_user = conversation.get_other_participant(request.user)
    
    context = {
        'conversation': conversation,
        'messages': messages_list,
    }
    return render(request, 'messaging/conversation_detail.html', context)

@login_required
def send_message(request, conversation_id):
    """Send a message in a conversation"""
    if request.method == 'POST':
        conversation = get_object_or_404(
            Conversation.objects.filter(
                id=conversation_id, participants=request.user
            )
        )
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            # Update conversation timestamp
            conversation.save()  # This will update the updated_at field
            
            if request.headers.get('HX-Request'):
                # Return the message HTML for HTMX
                return render(request, 'partials/message_item.html', {'message': message})
            else:
                messages.success(request, 'Message sent successfully!')
        else:
            if request.headers.get('HX-Request'):
                return HttpResponse('<div class="alert alert-error">Message cannot be empty</div>')
            else:
                messages.error(request, 'Message cannot be empty')
    
    return redirect('messaging:conversation_detail', conversation_id=conversation_id)

@login_required
def start_conversation(request):
    """Start a new conversation"""
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        property_id = request.POST.get('property_id')
        initial_message = request.POST.get('message', '').strip()
        
        if not recipient_id or not initial_message:
            if request.headers.get('HX-Request'):
                return HttpResponse('<div class="alert alert-error">Recipient and message are required</div>')
            messages.error(request, 'Recipient and message are required')
            return redirect('messaging:conversation_list')
        
        try:
            recipient = User.objects.get(id=recipient_id)
            property_obj = None
            
            if property_id:
                property_obj = Property.objects.get(id=property_id)
            
            # Check if conversation already exists
            existing_conversation = Conversation.objects.filter(
                property=property_obj
            ).filter(
                participants=request.user
            ).filter(
                participants=recipient
            ).first()
            
            if existing_conversation:
                conversation = existing_conversation
            else:
                # Create new conversation
                conversation = Conversation.objects.create(
                    subject=f"Conversation with {recipient.username}",
                    property=property_obj
                )
                conversation.participants.add(request.user, recipient)
            
            # Send initial message
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=initial_message
            )
            
            if request.headers.get('HX-Request'):
                # Render the conversation detail partial for real-time swap
                messages_list = conversation.messages.select_related('sender').order_by('created_at')
                conversation.other_user = conversation.get_other_participant(request.user)
                context = {
                    'conversation': conversation,
                    'messages': messages_list,
                }
                return render(request, 'messaging/conversation_detail.html', context)
            else:
                messages.success(request, 'Message sent successfully!')
                return redirect('messaging:conversation_detail', conversation_id=conversation.id)
            
        except User.DoesNotExist:
            if request.headers.get('HX-Request'):
                return HttpResponse('<div class="alert alert-error">Recipient not found</div>')
            messages.error(request, 'Recipient not found')
        except Property.DoesNotExist:
            if request.headers.get('HX-Request'):
                return HttpResponse('<div class="alert alert-error">Property not found</div>')
            messages.error(request, 'Property not found')
        except Exception as e:
            if request.headers.get('HX-Request'):
                return HttpResponse('<div class="alert alert-error">An error occurred while sending the message</div>')
            messages.error(request, 'An error occurred while sending the message')
    
    return redirect('messaging:conversation_list')

@login_required
def mark_conversation_read(request, conversation_id):
    """Mark all messages in a conversation as read"""
    if request.method == 'POST':
        conversation = get_object_or_404(
            Conversation.objects.filter(
                participants=request.user,
                id=conversation_id
            )
        )
        
        # Mark all unread messages from other user as read
        conversation.messages.filter(
            ~Q(sender=request.user),
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})
