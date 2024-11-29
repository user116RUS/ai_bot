from django.db import models

import datetime
from datetime import timedelta


class Mode(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name="Название для юзеров",
        help_text="Н-р: Базовая"
    )
    model = models.CharField(max_length=50, verbose_name="Модель ИИ (vseGPT)")
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

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Модели ИИ'
        verbose_name_plural = 'Модели ИИ'


class User(models.Model):
    telegram_id = models.CharField(primary_key=True, max_length=50)
    balance = models.FloatField(
        verbose_name='Баланс в рублях',
        help_text='ВНИМАНИЕ: не менять без согласавания!'
    )
    name = models.CharField(
        max_length=35,
        verbose_name="Имя",
    )
    message_context = models.JSONField(
        verbose_name='История переписки пользователя',
        null=True,
        blank=True,
    )
    current_mode = models.ForeignKey(
        Mode,
        on_delete=models.SET_NULL,
        related_name='user',
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

    def save(self, *args, **kwargs):
        if self.pk and User.objects.filter(pk=self.pk).exists():
            previous_balance = User.objects.get(pk=self.pk).balance
            balance_change = self.balance - previous_balance
            if balance_change != 0:
                Transaction.objects.create(
                    user=self,
                    is_addition=balance_change > 0,
                    cash=abs(balance_change),
                    mode=self.current_mode,
                    comment="Пополнение баланса",
                )
        super().save(*args, **kwargs)


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


class Referal(models.Model):
    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пригласитель',
        related_name='referal'
    )
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.inviter.name

    class Meta:
        verbose_name = 'Реферал'
        verbose_name_plural = 'Рефералки'


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Покупатель',
        related_name='transaction'
    )
    is_addition = models.BooleanField(default=False)
    cash = models.FloatField(
        verbose_name="Изменение",
    )
    mode = models.ForeignKey(
        Mode,
        on_delete=models.SET_NULL,
        related_name='transaction',
        null=True,
        blank=True,
    )
    comment = models.CharField(max_length=50, verbose_name="Пояснение к пополнению")
    adding_time = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return str(self.mode)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def save(self, *args, **kwargs):
        if not self.adding_time:
            self.adding_time = datetime.datetime.now() + timedelta(hours=3)
        super().save(*args, **kwargs)
