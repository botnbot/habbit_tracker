from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Расширенная модель пользователя с поддержкой Telegram.
    """

    telegram_chat_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Telegram Chat ID",
        help_text="ID чата пользователя в Telegram для отправки уведомлений",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email or self.username
