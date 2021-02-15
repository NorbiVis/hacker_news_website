from django.urls import path
from .views import (
    home_page, register,login_view, logout_view, create_news, comment_news, account_info, account_detail,
    comments,like_news, welcome_page, past_news_view, like_comments, hide_news
)

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register, name="register"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('create_news', create_news, name="create_news"),
    path('comment_news/<int:news_id>', comment_news, name="comment_news"),
    path('account/', account_info, name="account_info"),
    path('account/<int:acc_id>', account_detail, name="account_detail"),
    path('comments/', comments, name="comments"),
    path('like/', like_news, name="like_news"),
    path('like_comments/', like_comments, name="like_comments"),
    path('welcome/', welcome_page, name="welcome_page"),
    path('past_news', past_news_view, name="past_news"),
    path('hide_news', hide_news, name="hide_news")
]