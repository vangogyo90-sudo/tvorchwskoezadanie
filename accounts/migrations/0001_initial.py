# Generated manually for the completed application.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("owner", "Владелец"),
                            ("veterinarian", "Ветеринар"),
                            ("admin", "Администратор"),
                        ],
                        default="owner",
                        max_length=24,
                        verbose_name="Роль",
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=40, verbose_name="Телефон")),
                ("clinic", models.CharField(blank=True, max_length=160, verbose_name="Клиника")),
                ("notes", models.TextField(blank=True, verbose_name="Заметки")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлен")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "профиль",
                "verbose_name_plural": "профили",
                "ordering": ("user__username",),
            },
        ),
    ]
