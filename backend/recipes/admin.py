from django.contrib import admin
from django.db.models import Count
from users.models import Follow

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through


class TagsInLine(admin.TabularInline):
    model = Tag.recipes.through


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInLine, TagsInLine
    ]
    list_display = (
        'id', 'name', 'author', 'text', 'pub_date', 'favorite_count'
    )
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags', 'pub_date')
    empty_value_display = '---'

    def favorite_count(self, obj):
        return obj.obj_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            obj_count=Count('favorite', distinct=True)
        )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '---'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'color', 'slug'
    )
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empy_value_display = '---'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('id', 'user', 'recipe')
    empy_value_display = '---'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'recipe'
    )
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empy_value_display = '---'


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'following'
    )
    search_fields = ('user')
    list_filter = ('user', 'following')
    empty_value_display = '---'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Follow, FollowAdmin)
