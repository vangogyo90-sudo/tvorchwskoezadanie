from django.contrib import admin

from .models import Cat


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "sex", "breed", "birth_date", "updated_at")
    list_filter = ("sex", "created_at")
    search_fields = ("name", "owner__username", "breed", "color")

# Register your models here.
