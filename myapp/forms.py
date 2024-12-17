from django import forms 
from .models import Notice_board,Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class NoticeForm(forms.ModelForm):
    
    class Meta:
        model = Notice_board
        fields = ('title', 'description', 'image', 'price')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User()
        fields = ['username', 'password']



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        required=False,
        label="Поиск по названию",
        widget=forms.TextInput(attrs={"placeholder": "Введите название"})
    )