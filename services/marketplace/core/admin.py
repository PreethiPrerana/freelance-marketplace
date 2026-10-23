from django.contrib import admin
from .models import JobCategory, Job, Proposal, Contract
admin.site.register([JobCategory, Job, Proposal, Contract])
