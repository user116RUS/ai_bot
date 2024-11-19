from django.db import models


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
    telegram_id = models.IntegerField(primary_key=True)
    balance = models.FloatField(
        verbose_name='Баланс в рублях',
        help_text='ВНИМАНИЕ: не менять без согласавания!'
    )
    name = models.CharField(
        max_length=35,
        verbose_name="Имя",
    )
    content_history = models.JSONField(
        verbose_name='История изменения денег',
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
