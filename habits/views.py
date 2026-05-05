from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from .models import Habit
from .serializers import HabitSerializer, HabitPublicSerializer


class HabitPagination(LimitOffsetPagination):
    """Пагинация: 5 привычек на страницу"""
    default_limit = 5
    max_limit = 100


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Права доступа: владелец может редактировать, остальные только читать"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками.
    """
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя"""
        return Habit.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='public')
    def public_habits(self, request):
        """
        Эндпоинт для получения списка публичных привычек.
        GET /api/habits/public/
        """
        public_habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = HabitPublicSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = HabitPublicSerializer(public_habits, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """При создании автоматически подставляется текущий пользователь"""
        serializer.save(user=self.request.user)