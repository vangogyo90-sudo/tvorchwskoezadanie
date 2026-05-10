from django.conf import settings
from django.db import models
from django.utils import timezone

from cats.models import Cat


class HealthPassport(models.Model):
    BLOOD_UNKNOWN = "unknown"
    BLOOD_A = "a"
    BLOOD_B = "b"
    BLOOD_AB = "ab"
    BLOOD_CHOICES = (
        (BLOOD_UNKNOWN, "Неизвестно"),
        (BLOOD_A, "A"),
        (BLOOD_B, "B"),
        (BLOOD_AB, "AB"),
    )

    cat = models.OneToOneField(Cat, on_delete=models.CASCADE, related_name="health_passport", verbose_name="Кот")
    microchip_number = models.CharField("Номер микрочипа", max_length=64, blank=True)
    blood_type = models.CharField("Группа крови", max_length=16, choices=BLOOD_CHOICES, default=BLOOD_UNKNOWN)
    sterilized = models.BooleanField("Стерилизован/кастрирован", default=False)
    weight_kg = models.DecimalField("Вес, кг", max_digits=5, decimal_places=2, blank=True, null=True)
    allergies = models.TextField("Аллергии", blank=True)
    chronic_conditions = models.TextField("Хронические заболевания", blank=True)
    veterinarian_name = models.CharField("Ветеринар", max_length=120, blank=True)
    clinic_phone = models.CharField("Телефон клиники", max_length=40, blank=True)
    emergency_notes = models.TextField("Экстренные заметки", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        ordering = ("cat__name",)
        verbose_name = "паспорт здоровья"
        verbose_name_plural = "паспорта здоровья"

    def __str__(self):
        return f"Паспорт здоровья: {self.cat.name}"


class HealthRecord(models.Model):
    TYPE_VACCINATION = "vaccination"
    TYPE_VISIT = "visit"
    TYPE_TREATMENT = "treatment"
    TYPE_MEDICATION = "medication"
    TYPE_ANALYSIS = "analysis"
    TYPE_WEIGHT = "weight"
    TYPE_NOTE = "note"
    RECORD_TYPE_CHOICES = (
        (TYPE_VACCINATION, "Вакцинация"),
        (TYPE_VISIT, "Визит к врачу"),
        (TYPE_TREATMENT, "Лечение"),
        (TYPE_MEDICATION, "Прием лекарств"),
        (TYPE_ANALYSIS, "Анализ"),
        (TYPE_WEIGHT, "Контроль веса"),
        (TYPE_NOTE, "Заметка"),
    )

    passport = models.ForeignKey(HealthPassport, on_delete=models.CASCADE, related_name="records", verbose_name="Паспорт")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="health_records",
        verbose_name="Автор",
    )
    record_type = models.CharField("Тип записи", max_length=24, choices=RECORD_TYPE_CHOICES, default=TYPE_NOTE)
    title = models.CharField("Название", max_length=160)
    event_date = models.DateField("Дата события", default=timezone.localdate)
    next_due_date = models.DateField("Следующий срок", blank=True, null=True)
    clinic = models.CharField("Клиника", max_length=160, blank=True)
    doctor = models.CharField("Врач", max_length=120, blank=True)
    weight_kg = models.DecimalField("Вес, кг", max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        ordering = ("-event_date", "-created_at")
        verbose_name = "запись здоровья"
        verbose_name_plural = "записи здоровья"

    def __str__(self):
        return f"{self.get_record_type_display()}: {self.title}"
