from django.urls import path
from . import views
from .feeds import LatestProjectsFeed

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/<slug:slug>/", views.project_detail, name="project_detail"),
    path("like/", views.project_like, name="like"),
    path("success", views.message_sent, name="message_sent"),
    path('feed/', LatestProjectsFeed(), name='project_feed'),
]