# Generated by Django 4.2.1 on 2023-06-10 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_follow_follow_unique_object'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписчик', 'verbose_name_plural': 'Подписчики'},
        ),
    ]
