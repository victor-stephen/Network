# Generated by Django 4.1.2 on 2023-03-04 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_alter_follow_followed_alter_follow_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
