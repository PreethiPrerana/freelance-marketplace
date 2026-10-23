from django.urls import path
from . import views
urlpatterns = [path("jobs/", views.jobs), path("jobs/<uuid:job_id>/", views.job_detail), path("proposals/", views.proposals), path("proposals/<uuid:proposal_id>/hire/", views.hire)]
