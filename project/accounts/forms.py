from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm  # импортировали класс формы, который предоставляет allauth, а также модель групп
from django.contrib.auth.models import Group
from django.core.mail import send_mail, mail_managers, mail_admins
from django.core.mail import EmailMultiAlternatives


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")


class CustomSignupForm(SignupForm):
    """Класс добавляет пользователя в группу, переопределенный метод save() выполняется при успешной регистрации"""
    def save(self, request):
        user = super().save(request)  # вызываем этот же метод класса-родителя, чтобы необходимые проверки и сохранение в модель User были выполнены.

        # при новых регистрациях, всем менеджерам из настроек проекта будет отправлено оповещение
        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        # при новой регистрации, всем администраторам из настроек проекта будет приходить оповещение
        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        # common_users = Group.objects.get(name="common users")  # мы получаем объект модели группы с названием common users
        # user.groups.add(common_users)                          # добавляем нового пользователя в эту группу
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
