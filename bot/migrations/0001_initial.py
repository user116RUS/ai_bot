
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Н-р: Базовая', max_length=35, verbose_name='Название для юзеров')),
                ('model', models.CharField(max_length=50, verbose_name='Модель ИИ (vseGPT)')),
                ('price', models.FloatField(help_text='Моржа на токены (стоимость * токены)', verbose_name='Стоимость токена')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='img/%Y/%m/%d', verbose_name='Фото для оформления покупки')),
                ('max_token', models.IntegerField(verbose_name='Максимальное количество токенов на запрос')),
                ('is_base', models.BooleanField(default=False, help_text='ВНИМАНИЕ: только 1 должена быть модель')),
            ],
            options={
                'verbose_name': 'Модели ИИ',
                'verbose_name_plural': 'Модели ИИ',
            },
        ),
        migrations.CreateModel(
            name='TrainingMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='img/%Y/%m/%d', verbose_name='Фото')),
                ('agree_text', models.CharField(help_text='Н-р: Понятно', max_length=25, verbose_name='Надпись на кнопке')),
            ],
            options={
                'verbose_name': 'Обучение',
                'verbose_name_plural': 'Обучения',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('telegram_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('balance', models.FloatField(help_text='ВНИМАНИЕ: не менять без согласавания!', verbose_name='Баланс в рублях')),
                ('name', models.CharField(max_length=35, verbose_name='Имя')),

                ('message_context', models.JSONField(blank=True, null=True, verbose_name='История переписки пользователя')),
                ('referal_id', models.CharField(max_length=50)),
                ('plan_end', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_admin', models.BooleanField(default=False)),

                ('current_mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='bot.mode')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователь',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_addition', models.BooleanField(default=False)),
                ('cash', models.FloatField(verbose_name='Изменение')),
                ('comment', models.CharField(max_length=50, verbose_name='Пояснение к пополнению')),
                ('adding_time', models.DateTimeField()),
                ('mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction', to='bot.mode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='bot.user', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
            },
        ),
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=10000, verbose_name='Текст промпта')),
                ('name', models.CharField(max_length=50, verbose_name='Название промпта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prompt', to='bot.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Промпт',
                'verbose_name_plural': 'Промпты',
            },
        ),
    ]
