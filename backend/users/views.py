from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from djoser.views import UserViewSet
from recipes.pagination import CustomPageNumberPagination
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Follow
from .serializers import CustomUserSerializer, SubscriptionSerializer


class CustomUserViewSet(UserViewSet):
    """
    Вьюсет для модели пользователя
    наследуется от djoser.views.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination

    @action(
        detail=False,
        methods=('get',),
        serializer_class=SubscriptionSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        """
        Генерация списка подписок пользователя.
        """
        user = self.request.user
        user_subscriptions = user.follower.all()
        authors = [item.author.id for item in user_subscriptions]
        queryset = CustomUser.objects.filter(pk__in=authors)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        """
        Реализация подписки на автора.
        """
        user = get_object_or_404(CustomUser, username=request.user.username)
        author = get_object_or_404(CustomUser, pk=id)

        if request.method == 'POST':
            if user == author:
                content = {'errors': 'Нельзя подписаться на себя'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            try:
                Follow.objects.create(user=user, author=author)
            except IntegrityError:
                content = {'errors': 'Вы уже подписаны на данного автора'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            follows = CustomUser.objects.all().filter(username=author)
            serializer = SubscriptionSerializer(
                follows,
                context={'request': request},
                many=True,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            try:
                subscription = Follow.objects.get(user=user, author=author)
            except ObjectDoesNotExist:
                content = {'errors': 'Вы не подписаны на данного автора'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return HttpResponse('Вы успешно отписаны от этого автора',
                                status=status.HTTP_204_NO_CONTENT)
