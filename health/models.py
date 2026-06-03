from cats.models import Cat
from django.db import models
from django.utils import timezone


class HealthPassport(models.Model):
    BLOOD_UNKNOWN = 'unknown'
    BLOOD_A = 'A'
    BLOOD_B = 'B'
    BLOOD_AB = 'AB'
    BLOOD_CHOICES = (
        (BLOOD_UNKNOWN, 'Неизвестно'),
        (BLOOD_A, 'A'),
        (BLOOD_B, 'B'),
        (BLOOD_AB, 'AB'),
    )

    cat = models.OneToOneField(Cat, on_delete=models.CASCADE, related_name='health_passport')
    microchip_number = models.CharField(max_length=64, blank=True, null=True)
    blood_type = models.CharField(max_length=8, choices=BLOOD_CHOICES, default=BLOOD_UNKNOWN)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    veterinarian_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('cat__name',)

    def __str__(self):
        return f"Passport: {self.cat.name}"


class HealthRecord(models.Model):
    TYPE_CHECKUP = 'checkup'
    TYPE_VACCINE = 'vaccine'
    TYPE_TREATMENT = 'treatment'
    TYPE_OTHER = 'other'
    RECORD_TYPE_CHOICES = (
        (TYPE_CHECKUP, 'Приём'),
        (TYPE_VACCINE, 'Вакцинация'),
        (TYPE_TREATMENT, 'Лечение'),
        (TYPE_OTHER, 'Другое'),
    )

    passport = models.ForeignKey(HealthPassport, on_delete=models.CASCADE, related_name='records')
    event_date = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    record_type = models.CharField(max_length=32, choices=RECORD_TYPE_CHOICES, default=TYPE_OTHER)
    # Optional links to clinic and doctor
    clinic = models.ForeignKey('Clinic', on_delete=models.SET_NULL, related_name='records', null=True, blank=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, related_name='records', null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_records')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-event_date', '-created_at')

    def __str__(self):
        return f"{self.get_record_type_display()} for {self.passport.cat.name} on {self.event_date}"


class Clinic(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    specialization = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} ({self.clinic.name if self.clinic else 'no clinic'})"


class Vaccine(models.Model):
    """Catalog of vaccines."""
    name = models.CharField(max_length=200, unique=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class VaccineAdministration(models.Model):
    """A record that a given vaccine was administered to a passport (cat)."""
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT, related_name='administrations')
    passport = models.ForeignKey(HealthPassport, on_delete=models.CASCADE, related_name='vaccine_administrations')
    administered_at = models.DateField()
    dose = models.CharField(max_length=100, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True, related_name='vaccine_administrations')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='vaccine_administrations')
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_vaccine_admins')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-administered_at',)
        unique_together = (('vaccine', 'passport', 'administered_at'),)

    def __str__(self):
        return f"{self.vaccine.name} for {self.passport.cat.name} on {self.administered_at}"
