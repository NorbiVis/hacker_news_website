from django.contrib import admin
from .models import News, Comment,Account, Like, Hide, ReplayComment

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Account)
admin.site.register(Like)
admin.site.register(Hide)
admin.site.register(ReplayComment)
