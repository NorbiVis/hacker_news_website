# Generated by Django 3.1.5 on 2021-02-10 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_auto_20210210_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='time',
            field=models.TimeField(auto_now_add=True, verbose_name="<class 'datetime.datetime'>"),
        ),
    ]