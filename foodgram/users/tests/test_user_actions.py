from django.test import TestCase, Client
from django.urls import reverse

from recipes.models import Follow, Favorite, WishList
from .factories import UserFactory, RecipeWithIngredientFactory


class UserActionsTest(TestCase):
    """
    Тесты поведения пользователя
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.author = UserFactory()
        cls.recipe = RecipeWithIngredientFactory()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(UserActionsTest.user)

    def test_unathorized_client(self):
        urls = [
            "/feed/", "/new_recipe/", "/favorite/", "/get_purchases/"
        ]
        for url in urls:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertRedirects(response, f"/auth/login/?next={url}")

    def test_follow(self):
        data = {"id": f"{UserActionsTest.author.id}"}
        response = self.authorized_client.post(
            reverse("add_subscription"), data=data,
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Follow.objects.filter(
            user=UserActionsTest.user,
            author=UserActionsTest.author).exists())

    def test_follow_delete(self):
        data = {"id": f"{UserActionsTest.author.id}"}
        self.authorized_client.post(
            reverse("add_subscription"), data=data,
            content_type='application/json')
        response = self.authorized_client.delete(
            reverse("remove_subscription", args=[UserActionsTest.author.id]),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Follow.objects.filter(
            user=UserActionsTest.user,
            author=UserActionsTest.author).exists())

    def test_favorite(self):
        data = {"id": f"{UserActionsTest.recipe.id}"}
        response = self.authorized_client.post(
            reverse("add_favorite"), data=data,
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(
            user=UserActionsTest.user,
            recipe=UserActionsTest.recipe).exists())

    def test_favorite_delete(self):
        data = {"id": f"{UserActionsTest.recipe.id}"}
        self.authorized_client.post(
            reverse("add_favorite"), data=data,
            content_type="application/json")
        response = self.authorized_client.delete(
            reverse("remove_favorite", args=[UserActionsTest.recipe.id]),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Follow.objects.filter(
            user=UserActionsTest.user,
            recipe=UserActionsTest.recipe).exists())