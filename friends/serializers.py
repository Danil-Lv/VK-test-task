from rest_framework import serializers

from .models import User, Application


class ApplicationSerializer(serializers.ModelSerializer):
    """Заявка в друзья"""

    class Meta:
        model = Application
        fields = ('sender', 'recipient',)
        read_only_fields = ('sender', 'recipient',)


class ProfileSerializer(serializers.ModelSerializer):
    """Профиль владельца"""

    # submitted_applications = ApplicationSerializer(read_only=True)
    # received_applications = ApplicationSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'friends',
                  'submitted_applications',
                  'received_applications',
                  )


class AnotherProfileSerializer(ProfileSerializer):
    """Профиль другого пользователя"""
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

        app = Application.objects.filter(sender=user, recipient=instance)
        if app.exists():
            status = ['Отправлена заявка в друзья', app[0].id]
            return status

        app = Application.objects.filter(sender=user, recipient=instance)
        if Application.objects.filter(sender=instance, recipient=user).exists():
            status = ['Получена заявка в друзья', app[0].id]

        return status

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'status',
                  'first_name',
                  'last_name',
                  'friends',

                  )
