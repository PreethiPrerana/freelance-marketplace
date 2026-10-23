import uuid
from django.db import models
class FreelancerProfile(models.Model):
 user_id=models.UUIDField(unique=True, db_index=True)
 title=models.CharField(max_length=160, blank=True)
 overview=models.TextField(blank=True)
 hourly_rate=models.DecimalField(max_digits=10, decimal_places=2, default=0)
 experience_years=models.PositiveSmallIntegerField(default=0)
 skills=models.JSONField(default=list, blank=True)
 updated_at=models.DateTimeField(auto_now=True)
class ClientProfile(models.Model):
 user_id=models.UUIDField(unique=True, db_index=True)
 company_name=models.CharField(max_length=160, blank=True)
 description=models.TextField(blank=True)
 updated_at=models.DateTimeField(auto_now=True)
class PortfolioItem(models.Model):
 id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 user_id=models.UUIDField(db_index=True)
 title=models.CharField(max_length=160)
 description=models.TextField(blank=True)
 url=models.URLField(blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
