from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from cats.models import Cat

from .models import HealthPassport, HealthRecord
from accounts.models import Profile


User = get_user_model()


class HealthPassportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="owner", password="pass12345")
        self.other_user = User.objects.create_user(username="other", password="pass12345")
        self.cat = Cat.objects.create(owner=self.user, name="Муся")
        self.other_cat = Cat.objects.create(owner=self.other_user, name="Барс")
        self.client.force_authenticate(self.user)

    def test_user_creates_passport_for_own_cat(self):
        self.user.profile.role = Profile.ROLE_VETERINARIAN
        self.user.profile.save()
        response = self.client.post(
            reverse("health-passports-list"),
            {
                "cat_id": self.cat.id,
                "microchip_number": "643000000000001",
                "blood_type": HealthPassport.BLOOD_A,
                "sterilized": True,
                "weight_kg": "4.20",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        passport = HealthPassport.objects.get(cat=self.cat)
        self.assertEqual(passport.microchip_number, "643000000000001")

    def test_owner_cannot_create_passport(self):
        response = self.client.post(reverse("health-passports-list"), {"cat_id": self.other_cat.id}, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertFalse(HealthPassport.objects.filter(cat=self.other_cat).exists())

    def test_user_cannot_read_another_users_passport(self):
        passport = HealthPassport.objects.create(cat=self.other_cat)

        response = self.client.get(reverse("health-passports-detail", kwargs={"pk": passport.pk}))

        self.assertEqual(response.status_code, 404)


class HealthRecordApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="owner", password="pass12345")
        self.cat = Cat.objects.create(owner=self.user, name="Муся")
        self.passport = HealthPassport.objects.create(cat=self.cat)
        self.client.force_authenticate(self.user)

    def test_user_adds_health_record(self):
        self.user.profile.role = Profile.ROLE_VETERINARIAN
        self.user.profile.save()
        response = self.client.post(
            reverse("health-records-list"),
            {
                "passport_id": self.passport.id,
                "record_type": HealthRecord.TYPE_VACCINATION,
                "title": "Комплексная вакцинация",
                "event_date": "2026-05-10",
                "next_due_date": "2027-05-10",
                "clinic": "Добрый ветеринар",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        record = HealthRecord.objects.get()
        self.assertEqual(record.created_by, self.user)
        self.assertEqual(record.passport, self.passport)

    def test_next_due_date_cannot_be_before_event_date(self):
        self.user.profile.role = Profile.ROLE_VETERINARIAN
        self.user.profile.save()
        response = self.client.post(
            reverse("health-records-list"),
            {
                "passport_id": self.passport.id,
                "title": "Осмотр",
                "event_date": "2026-05-10",
                "next_due_date": "2026-05-01",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("next_due_date", response.data)

    def test_upcoming_records_endpoint(self):
        HealthRecord.objects.create(
            passport=self.passport,
            created_by=self.user,
            title="Повторная вакцинация",
            event_date=date(2026, 5, 10),
            next_due_date=date(2027, 5, 10),
        )

        response = self.client.get(reverse("health-records-upcoming"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

# Create your tests here.
