from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitAPITest(APITestCase):
    """Тесты API для привычек"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        # Получаем JWT токен
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_register_user(self):
        """Тест регистрации пользователя"""
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')

    def test_login_user(self):
        """Тест авторизации пользователя"""
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_create_habit(self):
        """Тест создания привычки"""
        data = {
            'place': 'Gym',
            'time': '08:00:00',
            'action': 'Workout',
            'duration': 90,
            'periodicity': 1
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Workout')
        self.assertEqual(response.data['place'], 'Gym')

    def test_create_habit_with_invalid_duration(self):
        """Тест создания привычки с неверной длительностью (больше 120)"""
        data = {
            'place': 'Gym',
            'time': '08:00:00',
            'action': 'Workout',
            'duration': 150,  # > 120
            'periodicity': 1
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_habits_pagination(self):
        """Тест пагинации (5 привычек на страницу)"""
        # Создаем 10 привычек
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                place=f'Place {i}',
                time='09:00:00',
                action=f'Action {i}',
                duration=30,
                periodicity=1
            )

        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['next'])

    def test_list_habits_with_limit_offset(self):
        """Тест пагинации с limit и offset"""
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                place=f'Place {i}',
                time='09:00:00',
                action=f'Action {i}',
                duration=30,
                periodicity=1
            )

        response = self.client.get('/api/habits/?limit=3&offset=0')
        self.assertEqual(len(response.data['results']), 3)

        response = self.client.get('/api/habits/?limit=3&offset=3')
        self.assertEqual(len(response.data['results']), 3)

    def test_retrieve_own_habit(self):
        """Тест получения конкретной привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='10:00:00',
            action='Read',
            duration=60,
            periodicity=1
        )

        response = self.client.get(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Read')

    def test_update_own_habit(self):
        """Тест обновления своей привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='10:00:00',
            action='Read',
            duration=60,
            periodicity=1
        )

        data = {'action': 'Updated action'}
        response = self.client.patch(f'/api/habits/{habit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Updated action')

    def test_delete_own_habit(self):
        """Тест удаления своей привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='10:00:00',
            action='Read',
            duration=60,
            periodicity=1
        )

        response = self.client.delete(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.filter(id=habit.id).count(), 0)

    def test_cannot_update_others_habit(self):
        """Тест: нельзя обновлять привычку другого пользователя"""
        other_user = User.objects.create_user(
            username='other',
            email='other@test.com',
            password='otherpass'
        )
        habit = Habit.objects.create(
            user=other_user,
            place='Office',
            time='11:00:00',
            action='Work',
            duration=120,
            periodicity=1
        )

        response = self.client.get(f'/api/habits/{habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habits_endpoint(self):
        """Тест эндпоинта публичных привычек"""
        Habit.objects.create(
            user=self.user,
            place='Public Park',
            time='12:00:00',
            action='Clean park',
            duration=30,
            periodicity=7,
            is_public=True
        )
        Habit.objects.create(
            user=self.user,
            place='Private',
            time='13:00:00',
            action='Private habit',
            duration=30,
            periodicity=1,
            is_public=False
        )

        # Снимаем авторизацию для проверки публичного эндпоинта
        self.client.credentials()
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['action'], 'Clean park')

    def test_unauthenticated_access(self):
        """Тест: неавторизованный пользователь не может получить список привычек"""
        self.client.credentials()
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)