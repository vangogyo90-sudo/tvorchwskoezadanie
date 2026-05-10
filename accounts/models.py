from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_OWNER = "owner"
    ROLE_VETERINARIAN = "veterinarian"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = (
        (ROLE_OWNER, "Владелец"),
        (ROLE_VETERINARIAN, "Ветеринар"),
        (ROLE_ADMIN, "Администратор"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField("Роль", max_length=24, choices=ROLE_CHOICES, default=ROLE_OWNER)
    phone = models.CharField("Телефон", max_length=40, blank=True)
    clinic = models.CharField("Клиника", max_length=160, blank=True)
    notes = models.TextField("Заметки", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        ordering = ("user__username",)
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
