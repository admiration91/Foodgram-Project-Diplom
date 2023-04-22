from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        subscribe = self.context.get('request')
        if subscribe and not subscribe.user.is_anonymous:
            return Follow.objects.filter(
                user=subscribe.user, following=obj
            ).exists()
        return


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = ('current_password', 'new_password')
