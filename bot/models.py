from django.db import models


class Mode(models.Model):
    name = models.CharField(max_length=35, verbose_name="Название")
    model = models.CharField(max_length=50, verbose_name="Модель ИИ")
    max_token = models.IntegerField()
    is_base = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Мод ИИ'
        verbose_name_plural = 'Моды ИИ'


class Prompt(models.Model):
    text = models.CharField(max_length=10000, verbose_name="Текст промпта")
    name = models.CharField(max_length=50, verbose_name="Название промпта")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промпт'
        verbose_name_plural = 'Промпты'


class User(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    name = models.CharField(
        max_length=35,
        verbose_name="Имя",
    )
    message_context = models.JSONField(
        verbose_name='История переписки пользователя',
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'


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


class UserMode(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_mode'
    )
    mode = models.ForeignKey(
        Mode,
        on_delete=models.CASCADE,
        verbose_name="Мод",
        related_name="user_mode"
    )
    requests_amount = models.IntegerField(verbose_name='Количество запросов')
    is_actual = models.BooleanField(default=False)


    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Юзер-Мод'
        verbose_name_plural = 'Юзер-Моды'
