import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache
from asgiref.sync import async_to_sync
import time
import logging

logger = logging.getLogger("chat")

PRESENCE_ONLINE_KEY = 'user_online_{}'
PRESENCE_LAST_SEEN_KEY = 'user_last_seen_{}'

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope["user"]

        logger.info(f"WebSocket connect: user={self.user}, is_authenticated={self.user.is_authenticated}")

        if self.user.is_anonymous:
            logger.warning("WebSocket closed: user is anonymous")
            await self.close()
        else:
            try:
                await self.set_user_online(self.user.id)
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()
                logger.info(f"WebSocket accepted for user {self.user.id}")
                # Broadcast presence update
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'presence_update',
                        'user_id': self.user.id,
                        'status': 'online',
                        'last_seen': None,
                    }
                )
            except Exception as e:
                logger.error(f"WebSocket connect error: {e}")
                await self.close()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnect: user={self.user}, code={close_code}")
        try:
            await self.set_user_offline(self.user.id)
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            # Broadcast presence update
            last_seen = await self.get_user_last_seen(self.user.id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'presence_update',
                    'user_id': self.user.id,
                    'status': 'offline',
                    'last_seen': last_seen,
                }
            )
        except Exception as e:
            logger.error(f"WebSocket disconnect error: {e}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get('type') == 'ping':
                # Update online status on ping
                await self.set_user_online(self.user.id)
                return
            message = data.get('message')
            user_id = self.user.id
            msg = await self.save_message(user_id, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': msg.content,
                    'sender': msg.sender.get_full_name(),
                    'timestamp': msg.created_at.strftime('%b %d, %Y %I:%M %p'),
                    'sender_id': msg.sender.id,
                }
            )
        except Exception as e:
            logger.error(f"WebSocket receive error: {e}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
            'sender_id': event['sender_id'],
        }))

    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'presence',
            'user_id': event['user_id'],
            'status': event['status'],
            'last_seen': event['last_seen'],
        }))

    @database_sync_to_async
    def save_message(self, user_id, message):
        from django.contrib.auth import get_user_model
        from .models import Conversation, Message
        User = get_user_model()
        user = User.objects.get(id=user_id)
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=user,
            content=message
        )

    @database_sync_to_async
    def set_user_online(self, user_id):
        cache.set(PRESENCE_ONLINE_KEY.format(user_id), True, timeout=60)
        cache.delete(PRESENCE_LAST_SEEN_KEY.format(user_id))

    @database_sync_to_async
    def set_user_offline(self, user_id):
        cache.delete(PRESENCE_ONLINE_KEY.format(user_id))
        cache.set(PRESENCE_LAST_SEEN_KEY.format(user_id), int(time.time()), timeout=3600*24)

    @database_sync_to_async
    def get_user_last_seen(self, user_id):
        ts = cache.get(PRESENCE_LAST_SEEN_KEY.format(user_id))
        if ts:
            return ts
        return None 