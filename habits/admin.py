from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "place", "time", "user", "duration", "is_public")
    list_filter = ("is_pleasant", "is_public", "periodicity")
    search_fields = ("action", "place", "user__username")
    readonly_fields = ("created_at", "updated_at")
    list_display_links = ("action",)
