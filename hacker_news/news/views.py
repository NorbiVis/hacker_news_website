from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm, LoginForm, AddNewsForm, CommentForm, AccountForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import News, Comment, Account, Like, Hide
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q

User = get_user_model()


def home_page(request):
    user = request.user
    # now = datetime.now()
    # account = Account.objects.all()
    # if not user :
    #     account = Account.objects.all()
    # else:
    #     account = Account.objects.get(user=user)
    allnews= News.objects.all().values_list('id', flat=True)
    print(allnews)
    hide = Hide.objects.filter(user=user).values_list("id", flat=True)
    # filtrat = News.objects.all().exclude(Hide.objects.filter(user=user))
    # query = (Q(Hide.objects.filter(user=user) | Q(News.objects.all())))
    print(hide)
    hide_id = Hide.objects.filter(user=user)
    hide_list=[]
    for line in hide_id:
        hide_list.append(line.news.id)
    print(hide_id)

    news = News.objects.all().exclude(id__in = hide_list) #not in
    news_id = news.values_list('id', flat=True)
    print(news_id)

    return render(request, 'news/home_page.html', {
        "news": news,
        "user": user,
        # "query": query,

    })


def account_detail(request, acc_id):
    account = Account.objects.get(pk=acc_id)
    return render(request, 'news/account_detail.html', {
        "account": account
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
    return redirect('home_page')


def like_comments(request):
    user = request.user
    news_id = request.POST.get('news_id')
    news_obj = News.objects.get(id=news_id)
    if request.method == "POST":
        print(news_obj)
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


@login_required
def account_info(request):
    user = User.objects.get(username=request.user)
    form = AccountForm(request.POST or None)
    # qs = Account.objects.all()
    qs = Account.objects.filter(user=user)
    # print(user)
    # print(user.id)
    # print(qs)
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
            # obj.user = user
            obj.save()

    return render(request, 'news/account_info.html', {
        "form": form,
        "user": user
    })


def comments(request):
    comments = Comment.objects.all()
    return render(request, 'news/comments.html', {
        'comments': comments
    })


@login_required
def comment_news(request, news_id):
    user = User.objects.get(username=request.user)
    news = News.objects.get(pk=news_id)
    print(news)
    print(user)

    comments = Comment.objects.filter(news=news.id)


    commentscount = Comment.objects.filter(news=news.id).count()
    form = CommentForm(request.POST or None)
    # if request.method == "POST":
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
        "counts": commentscount
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
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        try:
            user = User.objects.create_user(username, email, password)
        except:
            user = None
        return redirect("home_page")

    return render(request, 'news/register.html', {
        'form': form
    })


def login_view(request):  # cum as putea verifica de cate ori a incercat sa se logheze
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
    today = datetime.today()
    print(today)
    past_news = News.objects.filter(time__gt=datetime(2021, 2, 12,00,00,00))
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
