# Generated by Django 3.1.5 on 2021-02-16 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_auto_20210215_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_comment',
            field=models.ManyToManyField(blank=True, default=None, related_name='comment', to='news.Comment'),
        ),
    ]