from django.db import models
from django import utils

import datetime
from datetime import timedelta

class Mode(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name='Название для юзеров',
        help_text='Н-р: Базовая'
    )
    model = models.CharField(
        max_length=50,
        verbose_name='Модель ИИ (vseGPT)',
        help_text='openai/gpt-4o-mini'
    )
    price = models.FloatField(
        verbose_name="Стоимость токена",
        help_text="Моржа на токены (стоимость * токены)"
    )
    photo = models.ImageField(
        upload_to='img/%Y/%m/%d',
        verbose_name="Фото для оформления покупки",
        null=True,
        blank=True,
    )
    max_token = models.IntegerField(verbose_name="Максимальное количество токенов на запрос")
    is_base = models.BooleanField(
        default=False,
        help_text="ВНИМАНИЕ: только 1 должена быть модель"
    )
    daily_quota = models.PositiveIntegerField(
        verbose_name='Суточная квота для подписчиков'
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Модели ИИ'
        verbose_name_plural = 'Модели ИИ'


class User(models.Model):
    telegram_id = models.CharField(
        primary_key=True,
        max_length=50
    )
    balance = models.FloatField(
        verbose_name='Баланс в рублях',
        help_text='ВНИМАНИЕ: не менять без согласавания!'
    )
    name = models.CharField(
        max_length=35,
        verbose_name='Имя',
    )
    mode = models.CharField(
        max_length=35,
        verbose_name='Режим пользователя base/doc',
        help_text='Напиши base по умолчанию',
        default='base'
    )
    message_context = models.JSONField(
        verbose_name='История переписки пользователя',
        null=True,
        blank=True,
    )
    referral_id = models.CharField(
        max_length=50,
        verbose_name='Реферальный ID пользователя',
        blank=True,
        null=True,
    )
    current_mode = models.ForeignKey(
        Mode,
        on_delete=models.SET_NULL,
        related_name='user',
        null=True,
        blank=True,
    )
    plan_end = models.DateTimeField(
        verbose_name='Когда кончается подписка'
    )
    is_admin = models.BooleanField(default=False)
    is_trained = models.BooleanField(default=False)
    has_plan = models.BooleanField(default=False)
    ai_response = models.TextField(
        verbose_name='Ответ ИИ',
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save_balance(self, comment: str, type: str):
        if self.pk and User.objects.filter(pk=self.pk).exists():
            previous_balance = User.objects.get(pk=self.pk).balance
            balance_change = self.balance - previous_balance
            mode = self.current_mode
            if balance_change >= 0:
                mode = None
            Transaction.objects.create(
                user=self,
                type=type,
                cash=balance_change,
                mode=mode,
                comment=comment,
                adding_time=datetime.datetime.now() + timedelta(hours=3)
            )


class UserMode(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Юзер',
        related_name='user_mode',
    )
    mode = models.ForeignKey(
        Mode,
        on_delete=models.CASCADE,
        verbose_name='Режим',
        related_name='user_mode',
    )
    quota = models.PositiveIntegerField(
        default=0,
        verbose_name='Квота для пользователя'
    )

    def __str__(self):
        return f'{self.user.name} - {self.mode.name} Quota: {self.quota}'


class Prompt(models.Model):
    text = models.CharField(max_length=10000, verbose_name="Текст промпта")
    name = models.CharField(max_length=50, verbose_name="Название промпта")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='prompt'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промпт'
        verbose_name_plural = 'Промпты'


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
        related_name='transaction',
    )
    cash = models.FloatField(
        verbose_name="Изменение",
    )
    type = models.CharField(
        help_text='Хранить credit/debit/none. credit - мы потратили свои деньги. debit - мы получили деньги. none - другое',
        verbose_name="Тип транзакции",
        max_length=200,
    )
    comment = models.CharField(max_length=50, verbose_name="Пояснение к пополнению")
    mode = models.ForeignKey(
        Mode,
        on_delete=models.SET_NULL,
        related_name='transaction',
        null=True,
        blank=True,
    )
    adding_time = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return str(self.comment)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'



class TrainingMaterial(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    photo = models.CharField(
        verbose_name="Фото",
        null=True,
        blank=True,
        max_length=500,
    )
    agree_text = models.CharField(
        max_length=25,
        verbose_name='Надпись на кнопке',
        help_text='Н-р: Понятно',
    )
    numeration = models.PositiveIntegerField(
        verbose_name="Номер текста",
        help_text="Введите порядковый номер вопроса. Важно не прерывать цепочку! Вводить по порядку."
    )

    class Meta:
        verbose_name = 'Обучение'
        verbose_name_plural = 'Обучения'

    def __str__(self):
        return self.title