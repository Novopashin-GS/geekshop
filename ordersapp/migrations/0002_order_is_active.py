# Generated by Django 3.2 on 2022-01-26 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
