from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


def validate_duration(value):
    """Валидатор: время выполнения не более 120 секунд"""
    if value < 1:
        raise ValidationError('Время выполнения не может быть меньше 1 секунды')
    if value > 120:
        raise ValidationError('Время выполнения не должно превышать 120 секунд')
    return value


def validate_periodicity(value):
    """Валидатор: периодичность от 1 до 7 дней"""
    if value < 1 or value > 7:
        raise ValidationError('Периодичность должна быть от 1 до 7 дней')
    return value


def validate_reward_and_related_habit(reward, related_habit, is_pleasant):
    """
    Валидатор: правила для reward и related_habit
    1. Нельзя одновременно указывать reward и related_habit
    2. У приятной привычки не может быть reward или related_habit
    3. related_habit должна быть приятной привычкой
    """
    if reward and related_habit:
        raise ValidationError(
            'Нельзя одновременно указывать вознаграждение и связанную привычку'
        )

    if is_pleasant and (reward or related_habit):
        raise ValidationError(
            'Приятная привычка не может иметь вознаграждение или связанную привычку'
        )

    if related_habit and not related_habit.is_pleasant:
        raise ValidationError(
            'Связанная привычка должна быть приятной'
        )