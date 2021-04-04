import factory
from django.core.files.base import ContentFile

from recipes.models import Recipe, Ingredient, RecipeIngredient, Tag
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("email")
    email = username
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    title = "title"
    dimension = "dimension"


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    author = factory.SubFactory(UserFactory)
    title = "testtitle"
    description = "description"
    cooking_time = 10
    image = factory.LazyAttribute(
            lambda _: ContentFile(
                factory.django.ImageField()._make_data(
                    {'width': 1024, 'height': 768}
                ), 'example.jpg'
            )
        )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for topping in extracted:
                self.toppings.add(topping)


class RecipeInredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    recipe = factory.SubFactory(RecipeFactory)
    ingredient = factory.SubFactory(IngredientFactory)
    amount = 50


class RecipeWithIngredientFactory(RecipeFactory):
    recipe = factory.RelatedFactory(RecipeInredientFactory, "recipe")
