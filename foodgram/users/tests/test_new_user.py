from django.test import TestCase, Client
from django.urls import reverse

from users.models import User
# создание нового пользователя правильный/неправильный email
# после регистрации отправляет на главную страницу сразу
# доступ к about, technologies
# follow
# favorite
# shoplist
# добавить в покупки
class UserRegistrationTest(TestCase):
    """
    Регистрация нового пользователя
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create(
            username="testuser",
            email="newemail@google.com",
            password="testpassword")

    def setUp(self):
        self.client = Client()
        self.url = reverse("signup")

    def test_registration(self):
        data = {
            "username": "cyberdas", "email": "test@mail.ru", "password1": "testpassword",
            "password2": "testpassword", "first_name": "Daniil"
            }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_registration_email_fail(self):
        data = {
            "username": "cyberdas", "email": "newemail@google.com", "password1": "testpassword",
            "password2": "testpassword", "first_name": "Daniil"
            }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertFormError(response, "form", "email", "Данный email уже занят")

    def test_login(self):  # создавать пользователя и логиниться
        self.client.login()
        response = self.client.get(self.url)
        self.assertContains(response, text="Избранное")

    def test_about_page(self):
        response = self.client.get("about/author")
        self.assertContains(response, "Избранное")

    def test_technologies_page(self):
        response = self.client.get(reverse("technologies"))
        self.assertContains(response, text="Использованные технологии")
