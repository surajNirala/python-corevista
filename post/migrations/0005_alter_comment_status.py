# Generated by Django 5.1.2 on 2024-10-23 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]