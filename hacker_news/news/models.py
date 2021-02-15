from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()
from django.contrib.humanize.templatetags import humanize


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, default=None, blank=True, related_name="like")

    # comment = models.ManyToManyField(Comment, blank=True )

    def __str__(self):
        return f" {self.id} {self.title}"


    def num_likes(self):
        return self.like.all().count()


class Like(models.Model):
    LIKE_CHOICES = (('Like', "Like"), ('Unlike', 'Unlike'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news')
    value = models.CharField(max_length=10, choices=LIKE_CHOICES, default="Like")

    def __str__(self):
        return f"{self.news}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)
    text = models.TextField()


class Account(models.Model):
    boolean_choices = (
        (True, 'Yes'),
        (False, 'No'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE , primary_key=True)
    karma = models.CharField(max_length=3)
    about = models.TextField()
    showdead = models.BooleanField(default=False, choices=boolean_choices)
    nopro = models.BooleanField(default=False, choices=boolean_choices)

    def __str__(self):
        return f" {self.karma}, {self.user}, {self.about}"


class Hide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.news}"