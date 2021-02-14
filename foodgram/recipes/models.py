from django.db import models

from users.models import User


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Название ингредиента')
    dimension = models.CharField(
        max_length=300, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name='Название тэга')
    slug = models.SlugField(
        unique=True, max_length=100, blank=True, null=True, verbose_name='Тэг')
    color = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author_recipes',
        verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes', through='RecipeIngredient')
    tags = models.ManyToManyField(
        Tag, related_name='tag_recipes', verbose_name='Теги')
    cooking_time = models.IntegerField(verbose_name='Время готовки')
    slug = models.SlugField(unique=True, blank=True, null=True)
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients',
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Пользователь')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author',)


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_recipe',
        verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class WishList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wishlist',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='wishlist_recipe',
        verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
