# Generated by Django 5.1.2 on 2024-10-18 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='user',
        ),
    ]