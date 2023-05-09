from django.urls import path

from .views import (
    ProfileAPIView,
    ApplicationAPIView,
    ApplicationActionAPIView,
)

urlpatterns = [
    path('profile/<int:pk>/', ProfileAPIView.as_view()),  # GET Возвращает заданный профиль
    path('application/<int:pk>', ApplicationAPIView.as_view()),  # POST Создает заявку в друзья
    path('application/action/<int:application_pk>/', ApplicationActionAPIView.as_view()),
    # POST Принять или DELETE отклонить заявку. Прописать проверку - удалять и принимать может только получатель
    # path('friend/<int:pk>', FriendAPIView.as_view()),  # DELETE удалить из друзей
]
