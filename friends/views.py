from rest_framework import status, mixins
from rest_framework.generics import RetrieveAPIView, get_object_or_404, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProfileSerializer, ApplicationSerializer, AnotherProfileSerializer
from .models import User, Application


class ProfileAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs['user_pk'])

    def get_serializer(self, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['user_pk'])
        if user == self.request.user:
            self.serializer_class = ProfileSerializer
        elif user != self.request.user:
            self.serializer_class = AnotherProfileSerializer

        if self.request.method == 'POST':
            self.serializer_class = ApplicationSerializer
        return super().get_serializer(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удалить из друзей"""
        user = get_object_or_404(User, id=self.kwargs['user_pk'])
        if user == self.request.user:
            return Response('Нельзя удалить себя из друзей', status=status.HTTP_400_BAD_REQUEST)
        if user and self.request.user.friends.filter(id=user.id):
            self.request.user.friends.remove(user)
            return Response('Удалено', status=status.HTTP_200_OK)
        return Response('Ошибка при удалении', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_pk):
        """Отправить заявку в друзья"""
        recipient = User.objects.get(id=user_pk)

        if recipient == self.request.user:
            return Response('Нельзя отправить заявку самому себе')
        if Application.objects.filter(sender=request.user, recipient=recipient):
            return Response('Заявка уже была отправлена', status=status.HTTP_409_CONFLICT)
        if self.request.user.friends.filter(id=user_pk):
            return Response('Вы уже друзья', status=status.HTTP_400_BAD_REQUEST)
        if Application.objects.filter(sender=request.user, recipient=recipient) and \
                Application.objects.filter(sender=recipient, recipient=request.user):
            recipient.friends.add(self.request.user)
            return Response('Добавление', status=status.HTTP_200_OK)

        Application.objects.create(sender=request.user, recipient=recipient)

        return Response('Заявка отправлена', status=status.HTTP_201_CREATED)


class ApplicationActionAPIView(APIView):
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, application_pk):
        """Приняmь заявку в друзья"""
        application = get_object_or_404(Application, id=application_pk)
        if application.recipient == self.request.user:
            self.request.user.friends.add(application.sender)
            application.delete()
            return Response('Заявка принята', status=status.HTTP_200_OK)
        else:
            return Response('Вы не можете принять эту заявку')

    def delete(self, request, application_pk):
        """Отклонить заявку в друзья"""
        application = get_object_or_404(Application, id=application_pk)
        if application.recipient == self.request.user:
            application.delete()
            return Response('Заявка отклонена', status=status.HTTP_200_OK)
        else:
            return Response('Вы не можете отклонить эту заявку', status=status.HTTP_400_BAD_REQUEST)
