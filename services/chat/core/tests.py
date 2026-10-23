from django.test import TestCase
from .models import Conversation,Message
import uuid
class ChatModelTests(TestCase):
 def test_messages_are_persisted_for_conversation(self):
  c=Conversation.objects.create(client_id=uuid.uuid4(),freelancer_id=uuid.uuid4()); m=Message.objects.create(conversation=c,sender_id=c.client_id,body="Hello"); self.assertEqual(c.messages.get().body,"Hello")
