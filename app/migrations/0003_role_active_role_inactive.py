# Generated by Django 4.0.2 on 2022-10-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_role_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='inactive',
            field=models.BooleanField(default=False),
        ),
    ]
