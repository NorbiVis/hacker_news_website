# Generated by Django 3.1.5 on 2021-02-08 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20210208_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='url',
            field=models.URLField(null=True),
        ),
    ]