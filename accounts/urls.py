# accounts/urls.py

from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    CalculateAPIView,
    HistoryAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('calculate/', CalculateAPIView.as_view()),
    path('history/', HistoryAPIView.as_view()),
]