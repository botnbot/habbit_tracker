from rest_framework import serializers
from .models import Habit
from .validators import validate_reward_and_related_habit, validate_duration


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'related_habit', 'periodicity', 'reward', 'duration',
            'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, data):
        # Используем вынесенный валидатор
        validate_reward_and_related_habit(
            reward=data.get('reward'),
            related_habit=data.get('related_habit'),
            is_pleasant=data.get('is_pleasant', False)
        )
        return data

    def validate_duration(self, value):
        validate_duration(value)
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class HabitPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'periodicity', 'duration', 'created_at'
        ]