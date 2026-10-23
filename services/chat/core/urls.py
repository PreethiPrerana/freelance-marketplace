from django.urls import path
from . import views
urlpatterns = [path("conversations/", views.conversations), path("conversations/<uuid:conversation_id>/messages/", views.messages)]
