from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.urls import reverse

from foodgram.celery import app
from .utils import send_email_to_followers
from users.models import User
from foodgram.settings import EMAIL_HOST_USER


current = Site.objects.get_current()


@app.task
def send_email_task(username):
    email_list = send_email_to_followers(username)
    send_mail(
        "Новый рецепт",
        f"Пользователь {username} оставил новый рецепт",
        EMAIL_HOST_USER,
        email_list,
        fail_silently=False
    )


@app.task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    send_mail(
        subject="Регистрация на foodgram",
        message=f"Вы зарегестрировались на foodgram: {current}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
