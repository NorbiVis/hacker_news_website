# Generated by Django 3.1.5 on 2021-02-13 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_auto_20210213_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
