from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteListView, FavoriteView, IngredientsViewSet,
                    RecipeViewSet, ShoppingCartView, TagViewSet,
                    download_shopping_cart)

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view()),
    path('favorites/', FavoriteListView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view()),
    path('', include(router.urls)),
]
