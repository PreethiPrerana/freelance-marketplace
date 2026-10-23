import uuid
from django.db import models
class JobCategory(models.Model): name=models.CharField(max_length=100, unique=True)
class Job(models.Model):
 id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 client_id=models.UUIDField(db_index=True)
 title=models.CharField(max_length=180)
 description=models.TextField()
 category=models.CharField(max_length=100, blank=True)
 skills=models.JSONField(default=list, blank=True)
 budget=models.DecimalField(max_digits=12, decimal_places=2)
 status=models.CharField(max_length=16, choices=[("draft","Draft"),("published","Published"),("closed","Closed")],default="published", db_index=True)
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 class Meta: ordering=["-created_at"]
class Proposal(models.Model):
 id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name="proposals")
 freelancer_id=models.UUIDField(db_index=True)
 cover_letter=models.TextField()
 bid_amount=models.DecimalField(max_digits=12,decimal_places=2)
 status=models.CharField(max_length=16,choices=[("submitted","Submitted"),("accepted","Accepted"),("rejected","Rejected")],default="submitted",db_index=True)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: constraints=[models.UniqueConstraint(fields=["job","freelancer_id"],name="unique_freelancer_job_proposal")]
class Contract(models.Model):
 id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 job=models.ForeignKey(Job,on_delete=models.PROTECT)
 proposal=models.OneToOneField(Proposal,on_delete=models.PROTECT)
 client_id=models.UUIDField(db_index=True)
 freelancer_id=models.UUIDField(db_index=True)
 status=models.CharField(max_length=16,default="active")
 created_at=models.DateTimeField(auto_now_add=True)
