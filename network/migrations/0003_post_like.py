# Generated by Django 4.1.2 on 2023-02-21 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.IntegerField(default='0'),
        ),
    ]
