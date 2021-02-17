from django import forms
from django.contrib.auth import get_user_model, authenticate
from .models import News, Comment, Account, ReplayComment

User = get_user_model()


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('user',)


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'url', 'text')

    def clean(self):
        url = self.cleaned_data.get('url')
        text = self.cleaned_data.get('text')
        if not url and not text :
            raise forms.ValidationError("Fill url or text field.")  # de ce nu imi apare eroarea in pagina


    # def clean_text(self):
    #     url = self.cleaned_data.get('url')
    #     text = self.cleaned_data.get('text')
    #     if not url and not text :
    #         raise forms.ValidationError("Fill url or text field.")  # de ce nu imi apare eroarea in pagina
    #     return self.clean_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )


class ReplayCommentForm(forms.ModelForm):
    class Meta:
        model = ReplayComment
        fields = ('text', )


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=30)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="Password")


    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("Invalid username")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Invalid email")
        return email

    def clean(self):  # de ce nu merge cu clean_password
            # de ce trebuie neaparat? merge si fara
        pass1 = self.cleaned_data.get("password")
        pass2 = self.cleaned_data.get("password2")
        if pass1 != pass2:
            raise forms.ValidationError("Password don't match!")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact = username)
        if not qs.exists():
            raise forms.ValidationError("This is not a registered username")
        return username

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user_qs = User.objects.filter(username=username)
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Incorrect password")



