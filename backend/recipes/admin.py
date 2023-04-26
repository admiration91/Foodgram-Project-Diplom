from django.contrib import admin
from .models import Recipe, Ingredient, Tag

admin.site.register(Ingredient)
admin.site.register(Tag)


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through


class TagsInLine(admin.TabularInline):
    model = Tag.recipes.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInLine, TagsInLine
    ]
