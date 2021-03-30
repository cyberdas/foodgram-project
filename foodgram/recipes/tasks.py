import time
from celery import shared_task
from django.core.mail import send_mail

from foodgram.celery import app
from .utils import send_email_to_followers


@app.task
def send_email_task(username):
    email_list = send_email_to_followers(username)
    send_mail(
        "Новый рецепт",
        "Один из пользователей, на которых вы подписаны, составил новый рецепт",
        "webmaster@localhost",
        email_list,
        fail_silently=False
    )


@app.task
def test_task(a, b):
    c = a + b
    return c


@shared_task
def test_task_share(a, b):
    c = a + b
    return c
