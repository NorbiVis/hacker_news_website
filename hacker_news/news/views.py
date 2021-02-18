from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm, LoginForm, AddNewsForm, CommentForm, AccountForm, ReplayCommentForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import News, Comment, Account, Like, Hide, ReplayComment
from django.contrib.auth.decorators import login_required
from datetime import datetime

User = get_user_model()


def home_page(request):
    user = request.user
    news = News.objects.all()
    # allnews= News.objects.all().values_list('id', flat=True)
    # hide = Hide.objects.filter(user=user).values_list("id", flat=True)
    hide_list = []
    if request.user.is_authenticated:
        hide_id = Hide.objects.filter(user=user)
        for line in hide_id:
            hide_list.append(line.news.id)
    hide_news = News.objects.all().exclude(id__in=hide_list).order_by("-time")
    return render(request, 'news/home_page.html', {
        "hide_news": hide_news,
        "user": user,
        "news": news

    })


def like_news(request):
    user = request.user
    if request.method == "POST":
        news_id = request.POST.get('news_id')
        news_obj = News.objects.get(id=news_id)
        if user in news_obj.like.all():
            news_obj.like.remove(user)
        else:
            news_obj.like.add(user)

        like, created = Like.objects.get_or_create(user=user, news_id=news_id)

        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        like.save()
    return redirect("home_page")


def like_comments(request):
    user = request.user
    news_id = request.POST.get('news_id')
    news_obj = News.objects.get(id=news_id)
    if request.method == "POST":
        if user in news_obj.like.all():
            news_obj.like.remove(user)
        else:
            news_obj.like.add(user)

        like, created = Like.objects.get_or_create(user=user, news_id=news_id)

        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        like.save()
    return HttpResponseRedirect(reverse('comment_news', args=(news_id,)))


def account_detail(request, pk):
    account = Account.objects.get(user_id=pk)
    print(account)
    return render(request, 'news/account_detail.html', {
        "account": account
    })


@login_required
def account_info(request):
    user = User.objects.get(username=request.user)
    form = AccountForm(request.POST or None)
    qs = Account.objects.filter(user=user)
    if qs.exists():
        karma = request.POST.get('karma')
        about = request.POST.get('about')
        showdead = request.POST.get('showdead')
        nopro = request.POST.get('nopro')
        if form.is_valid():
            account = qs.first()
            account.user = user
            print(account.user)
            account.karma = karma
            account.about = about
            account.showdead = showdead
            account.nopro = nopro
            account.save()
    else:
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()

    return render(request, 'news/account_info.html', {
        "form": form,
        "user": user
    })


def comments(request):
    comments = Comment.objects.all().order_by("-time")
    return render(request, 'news/comments.html', {
        'comments': comments
    })


def comment_news(request, news_id):
    user = request.user
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
    news = News.objects.get(pk=news_id)
    comments = Comment.objects.filter(news=news.id).order_by("-time")
    comments_count = Comment.objects.filter(news=news.id).count()
    comments_id = Comment.objects.filter(news=news.id).values_list("id", flat=True)
    replay = ReplayComment.objects.filter(comment_id__in=comments_id).order_by("-time")
    form = CommentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.news = news
        obj.user = user
        obj.save()
        form = CommentForm()
        return HttpResponseRedirect(reverse('comment_news', args=(news.id,)))
    return render(request, 'news/comment_news.html', {
        "user": user,
        "news": news,
        "comments": comments,
        "form": form,
        "counts": comments_count,
        "replay": replay
    })


def comment_replay(request, pk):
    user = request.user
    comment = Comment.objects.get(pk=pk)
    print(comment.news)
    form = ReplayCommentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.comment = comment
        obj.user = user
        obj.news = comment.news
        obj.save()
        return HttpResponseRedirect(reverse('comment_news', args=(comment.news.id,)))
    return render(request, 'news/comment_replay.html', {
        "comment": comment,
        "form": form,
    })


@login_required
def create_news(request):
    form = AddNewsForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        print(request.user)
        obj.save()
        return redirect('home_page')
    return render(request, 'news/create_news.html', {
        'form': form
    })


def register(request):
    form = RegisterForm(request.POST or None)
    acc_form = AccountForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        try:
            user = User.objects.create_user(username, email, password)
        except:
            user = None
        account = Account.objects.create(user=user)
        return redirect("login_view")

    return render(request, 'news/register.html', {
        'form': form,
    })


def login_view(request):  
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('home_page')
    return render(request, 'news/login.html', {
        "form": form
    })


def logout_view(request):
    logout(request)
    return redirect('home_page')


def welcome_page(request):
    return render(request, 'news/welcome.html', {})


def past_news_view(request):
    today = datetime.now()
    print(today)
    print(today)
    past_news = News.objects.filter(time__lt=today).order_by("-time")
    return render(request, 'news/past_news.html', {
        "past_news": past_news
    })


def hide_news(request):
    user = request.user
    if request.method == "POST":
        hide_news = request.POST.get('hide_news')
        news_obj = News.objects.get(id=hide_news)
        obj = Hide.objects.filter(user=user, news=news_obj)
        if obj.exists():
            pass
        else:
            obj = Hide.objects.create(user=user, news=news_obj)
            obj.save()
    return redirect('home_page')


@login_required
def hidden_news_page(request):
    user = request.user
    hidden_news = Hide.objects.filter(user=user)
    return render(request, 'news/hidden_news.html', {
        "hidden_news": hidden_news
    })
