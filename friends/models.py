from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import AUTH_USER_MODEL


class Application(models.Model):
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_applications')
    recipient = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_applications')

    def __str__(self):
        return f'{self.sender} - {self.recipient}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class User(AbstractUser):
    applications = models.ManyToManyField('self', symmetrical=False, through='Application')
    friends = models.ManyToManyField('self')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
