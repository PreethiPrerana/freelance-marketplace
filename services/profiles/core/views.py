from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import FreelancerProfile, ClientProfile, PortfolioItem
@api_view(["GET","PUT"])
@permission_classes([IsAuthenticated])
def my_profile(request):
 uid=request.user.id; role=request.auth.get("role")
 model=FreelancerProfile if role=="freelancer" else ClientProfile
 obj=model.objects.filter(user_id=uid).first()
 if request.method=="GET":
  if not obj: return Response({"user_id":str(uid),"role":role})
  data={f.name:getattr(obj,f.name) for f in obj._meta.fields if f.name not in ("id",)}; data["role"]=role; return Response(data)
 data=request.data.copy(); data.pop("user_id",None); data.pop("role",None)
 allowed=({"title","overview","hourly_rate","experience_years","skills"} if role=="freelancer" else {"company_name","description"})
 data={k:v for k,v in data.items() if k in allowed}
 obj,created=model.objects.get_or_create(user_id=uid); [setattr(obj,k,v) for k,v in data.items()]; obj.save(); return Response({"user_id":str(uid),**data},status=201 if created else 200)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_detail(request,user_id):
 for model,role in ((FreelancerProfile,"freelancer"),(ClientProfile,"client")):
  obj=model.objects.filter(user_id=user_id).first()
  if obj:
   data={f.name:getattr(obj,f.name) for f in obj._meta.fields if f.name!="id"}; data["role"]=role; return Response(data)
 return Response({"detail":"Profile not found"},status=404)
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def portfolio(request):
 if request.method=="GET":
  qs=PortfolioItem.objects.filter(user_id=request.user.id).order_by("-created_at"); return Response(list(qs.values()))
 if request.auth.get("role")!="freelancer": return Response({"detail":"Freelancers only"},status=403)
 d=request.data; obj=PortfolioItem.objects.create(user_id=request.user.id,title=d.get("title",""),description=d.get("description",""),url=d.get("url","")); return Response({"id":str(obj.id),"title":obj.title,"description":obj.description,"url":obj.url},status=201)
