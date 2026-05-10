from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets

from cats.models import Cat
from health.models import HealthPassport, HealthRecord

from .forms import CatQuickForm, PassportQuickForm, RecordQuickForm, RegistrationForm, UserQuickForm
from .models import Profile
from .permissions import IsAdminRole, user_role
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminRole,)
    search_fields = ("username", "email", "first_name", "last_name", "profile__clinic")
    ordering_fields = ("username", "date_joined", "profile__role")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return get_user_model().objects.none()
        return get_user_model().objects.select_related("profile").order_by("username")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Регистрация завершена. Вы можете добавить своего питомца.")
        return redirect("owner-dashboard")

    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    role = user_role(request.user)
    if role == Profile.ROLE_ADMIN:
        return redirect("admin-dashboard")
    if role == Profile.ROLE_VETERINARIAN:
        return redirect("vet-dashboard")
    return redirect("owner-dashboard")


@login_required
def owner_dashboard(request):
    cats = Cat.objects.filter(owner=request.user).prefetch_related("health_passport__records")
    passports = HealthPassport.objects.filter(cat__owner=request.user).select_related("cat").annotate(records_total=Count("records"))
    records = HealthRecord.objects.filter(passport__cat__owner=request.user).select_related("passport", "passport__cat")[:18]
    cat_form = CatQuickForm()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_cat":
            cat_form = CatQuickForm(request.POST)
            if cat_form.is_valid():
                cat = cat_form.save(commit=False)
                cat.owner = request.user
                cat.save()
                messages.success(request, "Питомец добавлен.")
                return redirect("owner-dashboard")
            messages.error(request, "Не удалось добавить питомца.")
        else:
            messages.error(request, "Обычный пользователь может только просматривать данные и добавлять своего питомца.")

    context = {
        "role_name": "Владелец",
        "cats": cats,
        "passports": passports,
        "records": records,
        "cat_form": cat_form,
        "can_manage_cats": True,
        "can_delete_cats": False,
        "can_manage_records": False,
        "stats": {
            "коты": cats.count(),
            "паспорта": passports.count(),
            "записи": HealthRecord.objects.filter(passport__cat__owner=request.user).count(),
        },
    }
    return render(request, "accounts/owner_dashboard.html", context)


@login_required
def vet_dashboard(request):
    if user_role(request.user) not in (Profile.ROLE_VETERINARIAN, Profile.ROLE_ADMIN):
        return redirect("dashboard")

    passports = HealthPassport.objects.select_related("cat", "cat__owner").annotate(records_total=Count("records")).order_by("cat__name")
    passport_form = PassportQuickForm(cat_queryset=Cat.objects.filter(health_passport__isnull=True).select_related("owner"))
    record_form = RecordQuickForm(passport_queryset=HealthPassport.objects.select_related("cat"))

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_passport":
            passport_form = PassportQuickForm(request.POST, cat_queryset=Cat.objects.filter(health_passport__isnull=True))
            if passport_form.is_valid():
                passport_form.save()
                messages.success(request, "Паспорт пациента создан.")
                return redirect("vet-dashboard")
            messages.error(request, "Не удалось создать паспорт.")
        elif action == "delete_passport":
            passport = get_object_or_404(HealthPassport, pk=request.POST.get("passport_id"))
            passport.delete()
            messages.success(request, "Паспорт и его записи удалены.")
            return redirect("vet-dashboard")
        elif action == "create_record":
            record_form = RecordQuickForm(request.POST, passport_queryset=HealthPassport.objects.all())
            if record_form.is_valid():
                record = record_form.save(commit=False)
                record.created_by = request.user
                record.save()
                messages.success(request, "Назначение добавлено.")
                return redirect("vet-dashboard")
            messages.error(request, "Не удалось добавить назначение.")
        elif action == "delete_record":
            record = get_object_or_404(HealthRecord, pk=request.POST.get("record_id"))
            record.delete()
            messages.success(request, "Медицинская запись удалена.")
            return redirect("vet-dashboard")

    records = HealthRecord.objects.select_related("passport", "passport__cat", "created_by").order_by("-event_date", "-created_at")[:24]
    context = {
        "role_name": "Ветеринар",
        "records": records,
        "passports": passports[:18],
        "passport_form": passport_form,
        "record_form": record_form,
        "can_manage_passports": True,
        "can_manage_records": True,
        "stats": {
            "пациенты": Cat.objects.count(),
            "паспорта": HealthPassport.objects.count(),
            "записи": HealthRecord.objects.count(),
        },
    }
    return render(request, "accounts/vet_dashboard.html", context)


@login_required
def admin_dashboard(request):
    if user_role(request.user) != Profile.ROLE_ADMIN:
        return redirect("dashboard")

    user_form = UserQuickForm()
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_user":
            user_form = UserQuickForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Пользователь создан.")
                return redirect("admin-dashboard")
            messages.error(request, "Не удалось создать пользователя.")
        elif action == "delete_user":
            user = get_object_or_404(get_user_model(), pk=request.POST.get("user_id"))
            if user == request.user:
                messages.error(request, "Нельзя удалить собственную учетную запись из этой панели.")
            else:
                user.delete()
                messages.success(request, "Пользователь удален.")
                return redirect("admin-dashboard")

    users = get_user_model().objects.select_related("profile").annotate(cats_total=Count("cats")).order_by("username")
    records = HealthRecord.objects.select_related("passport", "passport__cat", "created_by")[:10]
    context = {
        "role_name": "Администратор",
        "users": users,
        "records": records,
        "user_form": user_form,
        "can_manage_users": True,
        "stats": {
            "пользователи": users.count(),
            "коты": Cat.objects.count(),
            "паспорта": HealthPassport.objects.count(),
            "записи": HealthRecord.objects.count(),
        },
    }
    return render(request, "accounts/admin_dashboard.html", context)
