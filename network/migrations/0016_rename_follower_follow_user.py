# Generated by Django 4.1.2 on 2023-03-06 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_rename_user_follow_follower'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='user',
        ),
    ]