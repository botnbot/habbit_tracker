import telebot
from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start - связывает Telegram с аккаунтом"""
    chat_id = str(message.chat.id)
    username = message.from_user.username

    # Ищем пользователя с таким же username
    try:
        user = User.objects.get(username=username)
        user.telegram_chat_id = chat_id
        user.save()

        bot.reply_to(
            message,
            f"🎉 Привет, {username}!\n\n"
            f"✅ Твой Telegram аккаунт привязан к пользователю '{username}'.\n\n"
            f"📋 Теперь ты будешь получать уведомления о привычках.\n"
            f"Чтобы это работало, убедись, что в приложении ты используешь тот же username."
        )
    except User.DoesNotExist:
        bot.reply_to(
            message,
            f"⚠️ Привет, {username}!\n\n"
            f"❌ Пользователь с username '{username}' не найден в системе.\n\n"
            f"📝 Зарегистрируйся в приложении с таким же username, "
            f"затем нажми /start еще раз."
        )


@bot.message_handler(commands=['help'])
def send_help(message):
    """Обработчик команды /help"""
    bot.reply_to(
        message,
        "🤖 *Помощь по боту*\n\n"
        "• /start - привязать Telegram к аккаунту\n"
        "• /help - показать эту справку\n"
        "• /status - проверить статус привязки\n\n"
        "_Вы будете получать автоматические напоминания о привычках_",
        parse_mode='Markdown'
    )


@bot.message_handler(commands=['status'])
def send_status(message):
    """Обработчик команды /status - проверка статуса"""
    username = message.from_user.username

    try:
        user = User.objects.get(username=username)
        if user.telegram_chat_id:
            bot.reply_to(
                message,
                f"✅ Статус: привязан!\n"
                f"👤 Пользователь: {user.username}\n"
                f"📧 Email: {user.email or 'не указан'}\n"
                f"💬 Telegram ID: {user.telegram_chat_id}"
            )
        else:
            bot.reply_to(
                message,
                f"⚠️ Статус: не привязан.\n"
                f"Нажми /start для привязки."
            )
    except User.DoesNotExist:
        bot.reply_to(
            message,
            f"❌ Пользователь '{username}' не найден.\n"
            f"Сначала зарегистрируйтесь в приложении."
        )


class Command(BaseCommand):
    help = 'Запуск Telegram бота для уведомлений о привычках'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🤖 Запуск Telegram бота...'))
        self.stdout.write(self.style.SUCCESS(f'📱 Имя бота: @{bot.get_me().username}'))
        self.stdout.write(self.style.WARNING('Нажмите Ctrl+C для остановки'))
        bot.infinity_polling()