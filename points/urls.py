from django.urls import path
from . import views

urlpatterns = [
    path('points/', views.PointAPIView.as_view(), name='points'),
]
