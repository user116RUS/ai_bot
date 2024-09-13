from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField(max_length=10, primary_key=True)
    name = models.CharField(max_length=35, verbose_name="Имя")
    # history =
    # UserRequest =


class Request(models.Model):
    name = models.CharField(max_length=35, verbose_name="Имя")
    model = models.CharField(max_length=20, verbose_name="Модель ИИ")
    max_token = models.IntegerField(max_length=8)


class Referal(models.Model):
    inviter = User.telegram_id
    is_used = models.BooleanField(default=False)


class UserRequest:
    ...


class Prompt(models.Model):
    text = models.CharField(max_length=500, verbose_name="Текст промпта")
    name = models.CharField(max_length=30, verbose_name="Название промпта")