from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm  # импортировали класс формы, который предоставляет allauth, а также модель групп
from django.contrib.auth.models import Group


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")


class CustomSignupForm(SignupForm):
    """Класс добавляет пользователя в группу, переопределенный метод save() выполняется при успешной регистрации"""
    def save(self, request):
        user = super().save(request)  # вызываем этот же метод класса-родителя, чтобы необходимые проверки и сохранение в модель User были выполнены.
        common_users = Group.objects.get(name="common users")  # мы получаем объект модели группы с названием common users
        user.groups.add(common_users)                          # добавляем нового пользователя в эту группу
        return user



    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
