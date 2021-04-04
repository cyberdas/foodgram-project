from django.test import TestCase, Client
from django.urls import reverse

from users.tests.factories import UserFactory, RecipeWithIngredientFactory


class RecipeActionsTest(TestCase):
    """
    Создание, редактирование, удаление рецепта
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.recipe = RecipeWithIngredientFactory()

    def setUp(self):
        self.client = Client()
        self.client.force_login(RecipeActionsTest.user)

    def test_new_recipe(self):
        form_data = {
            "title": "Новый рецепт",
            "description": "Описание",
            "cooking_time": "10",
        }
        response = self.client.post(reverse("new_recipe"), data=form_data)
        self.assertFormError(response, "form", "tags",  ["Это поле обязательно."])
        self.assertFormError(response, "form", "image", ["Это поле обязательно."])
        self.assertEqual(response.status_code, 200)

    def test_recipe_page(self):
        url = RecipeActionsTest.recipe.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{RecipeActionsTest.recipe.title}")
