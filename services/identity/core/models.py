import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
 id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
 ROLE_CHOICES = [("client", "Client"), ("freelancer", "Freelancer")]
 role = models.CharField(max_length=16, choices=ROLE_CHOICES)
 email = models.EmailField(unique=True)
 USERNAME_FIELD = "email"
 REQUIRED_FIELDS = ["username", "role"]
