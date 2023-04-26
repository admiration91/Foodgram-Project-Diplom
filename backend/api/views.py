import io
from os import path

from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Follow

from .filters import IngredientFilter, RecipeFilter
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, ReadRecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()
        if self.request.query_params.getlist('tags'):
            list = self.request.query_params.getlist('tags')
            queryset = queryset.filter(tags__slug__in=list).distinct()
        if self.request.query_params.get('is_favorited') == '1':
            queryset = queryset.filter(favorite__user=user)
        if self.request.query_params.get('is_in_shopping_cart') == '1':
            queryset = queryset.filter(shopping_cart__user=user)
        return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadRecipeSerializer
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                'request': self.request,
                'get_is_favorited': set(
                    Follow.objects.filter(
                        user__id=self.request.user.id
                    ).values_list(
                        'following_id', flat=True
                    )
                ),
                'get_is_in_shopping_cart': set(
                    ShoppingCart.objects.filter(
                        user__id=self.request.user.id
                    ).values_list(
                        'recipe_id', flat=True
                    )
                ),
                'subscriptions': set(
                    Follow.objects.filter(
                        user__id=self.request.user.id).values_list(
                            'following_id', flat=True
                    )
                )
            }
        )
        return context


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny, )


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientFilter
    search_fields = ['name', ]
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FavoriteView(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
        methods=['post'],
        detail=True,
    )
    def post(self, request, recipe_id):
        user = request.user
        data = {
            'user': user.id,
            'recipe': recipe_id,
        }
        context = {'request': request}
        serializer = FavoriteSerializer(data=data, context=context)
        if Favorite.objects.filter(user=user, recipe_id=recipe_id).exists():
            return Response(
                {'detail': 'Рецепт уже в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.create(user=user, recipe_id=recipe_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['delete'],
        detail=True,
    )
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'detail': 'Этого рецепта нет в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(
            {'detail': 'Рецепт удален'},
            status=status.HTTP_204_NO_CONTENT
        )


class FavoriteListView(ListAPIView):
    pagination_class = None
    serializer_class = FavoriteSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class ShoppingCartView(APIView):
    pagination_class = None

    @action(
        methods=['post'],
        detail=True,
    )
    def post(self, request, recipe_id):
        user = request.user
        data = {
            'user': user.id,
            'recipe': recipe_id,
        }
        context = {'request': request}
        serializer = ShoppingCartSerializer(
            data=data, context=context
        )
        if ShoppingCart.objects.filter(
            user=user,
            recipe_id=recipe_id
        ).exists():
            return Response(
                {'detail': 'Рецепт уже в корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.create(user=user, recipe_id=recipe_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['delete'],
        detail=True,
    )
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if not ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'detail': 'Этого рецепта нет в корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(
            {'detail': 'Рецепт удален'},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
def download_shopping_cart(request):
    app_path = path.realpath(path.dirname(__file__))
    font_path = path.join(app_path, 'fonts/Roboto-Italic.ttf')
    user = request.user
    shopping_cart = user.shopping_cart.all()
    buying_list = {}
    for record in shopping_cart:
        recipe = record.recipe
        ingredients = IngredientInRecipe.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in buying_list:
                buying_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                buying_list[name]['amount'] = (
                    buying_list[name]['amount'] + amount
                )
    wishlist = []
    for name, data in buying_list.items():
        wishlist.append(
            f'{name} - {data["amount"]} {data["measurement_unit"]}'
        )
    buffer = io.BytesIO()
    pdfmetrics.registerFont(
        TTFont('Roboto', font_path)
    )
    p = canvas.Canvas(buffer)
    x = 0.4 * inch
    y = 11 * inch
    p.setFont('Roboto', 14)
    p.drawString(x, y, 'Ваш список покупок сформирован Foodgram:')
    x += 15
    y -= 25
    for item in wishlist:
        p.setFont('Roboto', 12)
        p.drawString(x, y, item)
        y = y - 15
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Shopping.pdf')
