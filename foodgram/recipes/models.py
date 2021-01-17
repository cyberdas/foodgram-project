from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=300)

    def __str__(self):
        return self.title 


class Tags(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_recipes')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', through='RecipeIngredient') # рецепты, для которых нужен ингредиент
    tag = models.ManyToManyField(Tags)
    cooking_time = models.IntegerField()
    slug = models.SlugField(unique=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients') # все ингредиенты рецепта
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
