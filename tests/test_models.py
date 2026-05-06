from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели Habit"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_create_valid_habit(self):
        """Тест создания корректной привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='09:00',
            action='Morning exercise',
            duration=60,
            periodicity=1
        )
        self.assertEqual(habit.action, 'Morning exercise')
        self.assertEqual(habit.place, 'Home')
        self.assertEqual(habit.user, self.user)

    def test_duration_validation_max_120(self):
        """Тест: время выполнения не более 120 секунд"""
        habit = Habit(
            user=self.user,
            place='Gym',
            time='10:00',
            action='Workout',
            duration=130,  # > 120
            periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_duration_validation_min_1(self):
        """Тест: время выполнения не менее 1 секунды"""
        habit = Habit(
            user=self.user,
            place='Gym',
            time='10:00',
            action='Workout',
            duration=0,  # < 1
            periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_validation(self):
        """Тест: периодичность от 1 до 7 дней"""
        habit = Habit(
            user=self.user,
            place='Office',
            time='11:00',
            action='Drink water',
            duration=30,
            periodicity=10  # > 7
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_reward_and_related_habit_together(self):
        """Тест: нельзя одновременно указывать reward и related_habit"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Spa',
            time='12:00',
            action='Relax',
            duration=30,
            is_pleasant=True,
            periodicity=1
        )

        habit = Habit(
            user=self.user,
            place='Home',
            time='09:00',
            action='Clean',
            duration=60,
            reward='Chocolate',
            related_habit=pleasant_habit,
            periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_no_reward_or_related(self):
        """Тест: у приятной привычки не может быть reward или related_habit"""
        habit = Habit(
            user=self.user,
            place='Home',
            time='13:00',
            action='Nap',
            duration=60,
            is_pleasant=True,
            reward='Rest',  # Приятная привычка не может иметь reward
            periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_must_be_pleasant(self):
        """Тест: связанная привычка должна быть приятной"""
        # Создаем полезную привычку (не приятную)
        not_pleasant = Habit.objects.create(
            user=self.user,
            place='Office',
            time='14:00',
            action='Work',
            duration=120,
            is_pleasant=False,
            periodicity=1
        )

        habit = Habit(
            user=self.user,
            place='Home',
            time='09:00',
            action='Read',
            duration=30,
            related_habit=not_pleasant,
            periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_str_method(self):
        """Тест метода __str__"""
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='09:00',
            action='Morning routine',
            duration=60,
            periodicity=1
        )
        expected_str = f"{self.user.username}: Morning routine в 09:00:00"
        self.assertEqual(str(habit), expected_str)