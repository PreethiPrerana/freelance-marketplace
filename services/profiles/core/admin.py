from django.contrib import admin
from .models import FreelancerProfile, ClientProfile, PortfolioItem
admin.site.register([FreelancerProfile, ClientProfile, PortfolioItem])
