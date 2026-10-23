from django.urls import path
from . import views
urlpatterns = [path("auth/register/", views.register), path("auth/token/", views.TokenView.as_view()), path("auth/token/refresh/", views.RefreshView.as_view()), path("me/", views.me)]
