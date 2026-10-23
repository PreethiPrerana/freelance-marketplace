from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation,Message
def allowed(c,uid): return str(c.client_id)==str(uid) or str(c.freelancer_id)==str(uid)
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def conversations(request):
 if request.method=="GET":
  qs=Conversation.objects.filter(client_id=request.user.id) | Conversation.objects.filter(freelancer_id=request.user.id)
  return Response([{"id":str(c.id),"client_id":str(c.client_id),"freelancer_id":str(c.freelancer_id),"job_id":str(c.job_id) if c.job_id else None} for c in qs.distinct()])
 d=request.data; role=request.auth.get("role")
 if role=="client": client_id=request.user.id; freelancer_id=d.get("freelancer_id")
 elif role=="freelancer": client_id=d.get("client_id"); freelancer_id=request.user.id
 else: return Response({"detail":"Invalid role"},status=403)
 if not client_id or not freelancer_id: return Response({"detail":"Participant IDs are required"},status=400)
 try: c,created=Conversation.objects.get_or_create(client_id=client_id,freelancer_id=freelancer_id,job_id=d.get("job_id"))
 except IntegrityError: c=Conversation.objects.get(client_id=client_id,freelancer_id=freelancer_id,job_id=d.get("job_id")); created=False
 if not allowed(c,request.user.id): return Response({"detail":"Forbidden"},status=403)
 return Response({"id":str(c.id),"client_id":str(c.client_id),"freelancer_id":str(c.freelancer_id)},status=201 if created else 200)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def messages(request,conversation_id):
 c=get_object_or_404(Conversation,id=conversation_id)
 if not allowed(c,request.user.id): return Response({"detail":"Forbidden"},status=403)
 return Response([{"id":str(m.id),"sender_id":str(m.sender_id),"body":m.body,"created_at":m.created_at} for m in c.messages.all()[:200]])
