from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Job, Proposal, Contract
def job_data(j): return {"id":str(j.id),"client_id":str(j.client_id),"title":j.title,"description":j.description,"category":j.category,"skills":j.skills,"budget":str(j.budget),"status":j.status,"created_at":j.created_at}
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def jobs(request):
 if request.method=="GET":
  qs=Job.objects.filter(status="published")
  if request.auth.get("role")=="client": qs=Job.objects.filter(client_id=request.user.id)
  return Response([job_data(j) for j in qs[:100]])
 if request.auth.get("role")!="client": return Response({"detail":"Clients only"},status=403)
 d=request.data
 if not d.get("title") or not d.get("description"): return Response({"detail":"title and description are required"},status=400)
 j=Job.objects.create(client_id=request.user.id,title=d["title"],description=d["description"],category=d.get("category",""),skills=d.get("skills",[]),budget=d.get("budget",0),status=d.get("status","published")); return Response(job_data(j),status=201)
@api_view(["GET","PATCH"])
@permission_classes([IsAuthenticated])
def job_detail(request,job_id):
 j=get_object_or_404(Job,id=job_id)
 if request.method=="GET":
  if j.status!="published" and str(j.client_id)!=str(request.user.id): return Response({"detail":"Not found"},status=404)
  return Response(job_data(j))
 if str(j.client_id)!=str(request.user.id): return Response({"detail":"Forbidden"},status=403)
 for k in ("title","description","category","skills","budget","status"):
  if k in request.data: setattr(j,k,request.data[k])
 j.save(); return Response(job_data(j))
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def proposals(request):
 if request.method=="GET":
  qs=Proposal.objects.select_related("job")
  qs=qs.filter(job__client_id=request.user.id) if request.auth.get("role")=="client" else qs.filter(freelancer_id=request.user.id)
  return Response([{"id":str(p.id),"job_id":str(p.job_id),"job_title":p.job.title,"freelancer_id":str(p.freelancer_id),"cover_letter":p.cover_letter,"bid_amount":str(p.bid_amount),"status":p.status} for p in qs])
 if request.auth.get("role")!="freelancer": return Response({"detail":"Freelancers only"},status=403)
 d=request.data; j=get_object_or_404(Job,id=d.get("job_id"),status="published")
 p=Proposal.objects.create(job=j,freelancer_id=request.user.id,cover_letter=d.get("cover_letter",""),bid_amount=d.get("bid_amount",0)); return Response({"id":str(p.id),"job_id":str(j.id),"status":p.status},status=201)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def hire(request,proposal_id):
 if request.auth.get("role")!="client": return Response({"detail":"Clients only"},status=403)
 with transaction.atomic():
  p=get_object_or_404(Proposal.objects.select_for_update(),id=proposal_id,job__client_id=request.user.id)
  if p.status!="submitted": return Response({"detail":"Proposal is no longer available"},status=409)
  p.status="accepted"; p.save(update_fields=["status"]); Contract.objects.create(job=p.job,proposal=p,client_id=request.user.id,freelancer_id=p.freelancer_id); p.job.status="closed"; p.job.save(update_fields=["status"])
 return Response({"contract_id":str(Contract.objects.get(proposal=p).id),"proposal_id":str(p.id),"status":"active"},status=201)
