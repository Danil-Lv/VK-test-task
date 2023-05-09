from rest_framework import serializers

from .models import User, Application


class ProfileSerializer(serializers.ModelSerializer):
    """Профиль пользователя"""
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, instance):
        """Получение статуса дружбы"""
        status = 'Ничего'

        user = self.context['request'].user
        if user.is_anonymous:
            return status

        if user.friends.filter(id=instance.id).exists():
            status = 'В друзьях'
            return status

        if Application.objects.filter(sender=user, recipient=instance).exists():
            status = 'Отправлена заявка в друзья'
            return status

        if Application.objects.filter(sender=instance, recipient=user).exists():
            status = 'Получена заявка в друзья'

        return status

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'status',
                  'first_name',
                  'last_name',
                  'email',
                  'friends',
                  'submitted_applications',
                  'received_applications',
                  )


class AnotherProfileSerializer(ProfileSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'status',
                  'first_name',
                  'last_name',
                  'friends',

                  )


class ApplicationSerializer(serializers.ModelSerializer):
    """Заявка в друзья"""

    class Meta:
        model = Application
        fields = ('sender', 'recipient',)
        read_only_fields = ('sender', 'recipient',)
