from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Cat


User = get_user_model()


class CatApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="owner", password="pass12345")
        self.other_user = User.objects.create_user(username="other", password="pass12345")
        self.client.force_authenticate(self.user)

    def test_user_creates_cat(self):
        response = self.client.post(
            reverse("cats-list"),
            {"name": "Муся", "sex": Cat.SEX_FEMALE, "breed": "Сибирская"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Cat.objects.filter(owner=self.user, name="Муся").exists())

    def test_user_sees_only_own_cats(self):
        Cat.objects.create(owner=self.user, name="Муся")
        Cat.objects.create(owner=self.other_user, name="Барс")

        response = self.client.get(reverse("cats-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Муся")

# Create your tests here.
