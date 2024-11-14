# Generated by Django 4.1 on 2024-11-12 07:09

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
                ('price', models.IntegerField(help_text='Моржа на токены (стоимость * токены)', verbose_name='Стоимость токена')),
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
            name='User',
            fields=[
                ('telegram_id', models.IntegerField(primary_key=True, serialize=False)),
                ('balance', models.FloatField(help_text='ВНИМАНИЕ: не менять без согласавания!', verbose_name='Баланс в рублях')),
                ('name', models.CharField(max_length=35, verbose_name='Имя')),
                ('message_context', models.JSONField(blank=True, null=True, verbose_name='История переписки пользователя')),
                ('current_mode', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.mode')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователь',
            },
        ),
        migrations.CreateModel(
            name='Referal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_used', models.BooleanField(default=False)),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referal', to='bot.user', verbose_name='Пригласитель')),
            ],
            options={
                'verbose_name': 'Реферал',
                'verbose_name_plural': 'Рефералки',
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
