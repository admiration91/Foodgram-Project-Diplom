from api.serializers import ShortRecipeSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'following')
        read_only_fields = ('user', 'following')


class SubscriptionsSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        return obj.id in self.context['subscriptions']

    def get_recipes_count(self, obj):
        return obj.recipe.count()

    def get_recipes(self, obj):
        queryset = obj.recipe.all()
        serializer = ShortRecipeSerializer(
            queryset, many=True, required=True
        )
        return serializer.data
