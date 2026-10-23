import uuid
from django.db import models
class Conversation(models.Model):
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
 client_id=models.UUIDField(db_index=True)
 freelancer_id=models.UUIDField(db_index=True)
 job_id=models.UUIDField(null=True,blank=True,db_index=True)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: constraints=[models.UniqueConstraint(fields=["client_id","freelancer_id","job_id"],name="unique_conversation_participants_job")]
class Message(models.Model):
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
 conversation=models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name="messages")
 sender_id=models.UUIDField(db_index=True)
 body=models.TextField(max_length=5000)
 created_at=models.DateTimeField(auto_now_add=True,db_index=True)
 class Meta: ordering=["created_at"]
