from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe


class RecipeFilter(FilterSet):

    class Meta:
        model = Recipe
        fields = ('author', )


class IngredientFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
