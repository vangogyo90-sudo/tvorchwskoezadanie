from django.conf import settings
from django.db import models


class Cat(models.Model):
    SEX_MALE = "male"
    SEX_FEMALE = "female"
    SEX_UNKNOWN = "unknown"
    SEX_CHOICES = (
        (SEX_MALE, "Кот"),
        (SEX_FEMALE, "Кошка"),
        (SEX_UNKNOWN, "Неизвестно"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cats",
        verbose_name="Владелец",
    )
    name = models.CharField("Кличка", max_length=80)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    sex = models.CharField("Пол", max_length=16, choices=SEX_CHOICES, default=SEX_UNKNOWN)
    breed = models.CharField("Порода", max_length=120, blank=True)
    color = models.CharField("Окрас", max_length=80, blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "кот"
        verbose_name_plural = "коты"

    def __str__(self):
        return self.name
