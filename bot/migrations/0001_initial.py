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
                ('model', models.CharField(help_text='openai/gpt-4o-mini', max_length=50, verbose_name='Модель ИИ (vseGPT)')),
                ('price', models.FloatField(help_text='Моржа на токены (стоимость * токены)', verbose_name='Стоимость токена')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='img/%Y/%m/%d', verbose_name='Фото для оформления покупки')),
                ('max_token', models.IntegerField(verbose_name='Максимальное количество токенов на запрос')),
                ('is_base', models.BooleanField(default=False, help_text='ВНИМАНИЕ: только 1 должена быть модель')),
                ('daily_quota', models.PositiveIntegerField(verbose_name='Суточная квота для подписчиков')),
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
                ('photo', models.CharField(blank=True, max_length=500, null=True, verbose_name='Фото')),
                ('agree_text', models.CharField(help_text='Н-р: Понятно', max_length=25, verbose_name='Надпись на кнопке')),
                ('numeration', models.PositiveIntegerField(help_text='Введите порядковый номер вопроса. Важно не прерывать цепочку! Вводить по порядку.', verbose_name='Номер текста')),
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
                ('mode', models.CharField(default='base', help_text='Напиши base по умолчанию', max_length=35, verbose_name='Режим пользователя base/doc')),
                ('message_context', models.JSONField(blank=True, null=True, verbose_name='История переписки пользователя')),
                ('referral_id', models.CharField(max_length=50, verbose_name='Реферальный ID пользователя')),
                ('plan_end', models.DateTimeField(auto_now=True, verbose_name='Когда кончается подписка')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_trained', models.BooleanField(default=False)),
                ('has_plan', models.BooleanField(default=False)),
                ('ai_response', models.TextField(blank=True, null=True, verbose_name='Ответ ИИ')),
                ('current_mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='bot.mode')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quota', models.PositiveIntegerField(default=0, verbose_name='Квота для пользователя')),
            ],
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
