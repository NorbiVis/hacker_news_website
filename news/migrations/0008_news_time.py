# Generated by Django 3.1.5 on 2021-02-08 12:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20210208_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='time',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
