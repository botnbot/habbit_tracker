from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit"""

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate(self, data):
        """Валидация данных"""
        # 1. Нельзя одновременно указывать вознаграждение и связанную привычку
        if data.get("reward") and data.get("related_habit"):
            raise serializers.ValidationError(
                {
                    "non_field_errors": "Нельзя одновременно указывать вознаграждение и связанную привычку"
                }
            )

        # 2. У приятной привычки не может быть вознаграждения или связанной привычки
        if data.get("is_pleasant") and (
            data.get("reward") or data.get("related_habit")
        ):
            raise serializers.ValidationError(
                {
                    "is_pleasant": "Приятная привычка не может иметь вознаграждение или связанную привычку"
                }
            )

        # 3. Связанная привычка должна быть приятной
        related_habit = data.get("related_habit")
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                {"related_habit": "Связанная привычка должна быть приятной"}
            )

        return data

    def create(self, validated_data):
        """Создание привычки с текущим пользователем"""
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)


class HabitPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек (только чтение)"""

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "periodicity",
            "duration",
            "created_at",
        ]
