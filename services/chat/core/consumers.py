import json
import uuid
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Conversation,Message
class ChatConsumer(AsyncJsonWebsocketConsumer):
 async def connect(self):
  token=parse_qs(self.scope["query_string"].decode()).get("token",[None])[0]
  try:
   validated=JWTAuthentication().get_validated_token(token); self.user_id=str(validated["user_id"]); self.role=validated.get("role")
   self.conversation_id=uuid.UUID(self.scope["url_route"]["kwargs"]["conversation_id"])
   if not await self.is_member(): await self.close(code=4403); return
  except Exception: await self.close(code=4401); return
  self.group_name=f"conversation_{self.conversation_id.hex}"; await self.channel_layer.group_add(self.group_name,self.channel_name); await self.accept()
 async def disconnect(self,close_code):
  if hasattr(self,"group_name"): await self.channel_layer.group_discard(self.group_name,self.channel_name)
 async def receive_json(self,content,**kwargs):
  body=content.get("body","")
  if not isinstance(body,str) or not body.strip() or len(body)>5000: await self.send_json({"error":"Message must be 1-5000 characters"}); return
  msg=await self.save_message(body.strip())
  await self.channel_layer.group_send(self.group_name,{"type":"chat.message","message":msg})
 async def chat_message(self,event): await self.send_json(event["message"])
 @database_sync_to_async
 def is_member(self):
  return Conversation.objects.filter(id=self.conversation_id).filter(client_id=self.user_id).exists() or Conversation.objects.filter(id=self.conversation_id).filter(freelancer_id=self.user_id).exists()
 @database_sync_to_async
 def save_message(self,body):
  c=Conversation.objects.get(id=self.conversation_id); m=Message.objects.create(conversation=c,sender_id=self.user_id,body=body); return {"id":str(m.id),"sender_id":self.user_id,"body":m.body,"created_at":m.created_at.isoformat()}
