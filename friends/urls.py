from django.urls import path

from .views import (
    ProfileAPIView,
    ApplicationActionAPIView,
)

urlpatterns = [
    path('profile/<int:user_pk>/', ProfileAPIView.as_view()),
    path('application/<int:application_pk>/', ApplicationActionAPIView.as_view()),

]
