from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .custom_user import PasswordSerializer, UserSerializer
from .models import Follow
from .serializers import FollowSerializer, SubscriptionsSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                'request': self.request,
                'subscriptions': set(
                    Follow.objects.filter(
                        user_id=self.request.user.id).values_list(
                            'following_id', flat=True
                    )
                )
            }
        )
        return context

    @action(
        methods=['get', 'post'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        get_password = self.request.data['password']
        password = make_password(get_password)
        serializer.save(password=password)

    def perform_update(self, serializer):
        get_password = self.request.data['password']
        password = make_password(get_password)
        serializer.save(password=password)

    @action(
        methods=['post'],
        detail=False
    )
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                'Пароль успешно изменен',
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        follower = Follow.objects.filter(user=user)
        followers = []
        for follow in follower:
            followers.append(follow.following)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result = paginator.paginate_queryset(followers, request)
        serializer = SubscriptionsSerializer(
            result, many=True, context={
                'current_user': user,
                'request': request
            }
        )
        return paginator.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, pk=None):
        user = request.user
        following = get_object_or_404(User, pk=pk)
        follow = Follow.objects.filter(user=user, following=following)
        if request.method == 'POST':
            if follow.exists():
                return Response(
                    {'detail': 'Вы уже подписаны!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = Follow.objects.create(
                following=following, user=user
            )
            serializer = FollowSerializer(
                queryset,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow.delete()
        return Response(
            {'detail': 'Подписка удалена'},
            status=status.HTTP_204_NO_CONTENT
        )
