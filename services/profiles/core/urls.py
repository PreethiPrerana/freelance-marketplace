from django.urls import path
from . import views
urlpatterns = [path("profiles/me/", views.my_profile), path("profiles/<uuid:user_id>/", views.profile_detail), path("portfolio/", views.portfolio)]
