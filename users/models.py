from django.db import models
from django.contrib.auth.models import User


class Activation(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):

    STATUS = (
        (1, 'Студент'),
        (2, 'Преподователь'),
    )
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='Статус пользователя')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Профиль {self.user}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = 'Профиль пользователей'

