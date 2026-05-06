from celery import shared_task
from django.utils import timezone
from django.conf import settings
from .models import Habit
import telebot

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@shared_task
def send_habit_reminders():
    """
    Задача для отправки напоминаний о привычках.
    Запускается каждую минуту через Celery Beat.
    """
    now = timezone.now()
    current_time = now.time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        is_pleasant=False,
    )

    sent_count = 0
    for habit in habits:
        user = habit.user
        if not user.telegram_chat_id:
            continue

        message = f"🔔 Напоминание!\nДействие: {habit.action}\nМесто: {habit.place}"

        try:
            bot.send_message(user.telegram_chat_id, message)
            sent_count += 1
        except Exception as e:
            print(f"Ошибка: {e}")

    return f"Отправлено {sent_count} напоминаний"
