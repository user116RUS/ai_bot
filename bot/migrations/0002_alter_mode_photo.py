# Generated by Django 4.1 on 2024-10-03 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mode',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='img/%Y/%m/%d', verbose_name='Фото для оформления покупки'),
        ),
    ]
