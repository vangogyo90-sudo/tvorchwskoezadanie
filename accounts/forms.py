from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from cats.models import Cat
from health.models import HealthPassport, HealthRecord

from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=False)
    first_name = forms.CharField(label="Имя", required=False)
    last_name = forms.CharField(label="Фамилия", required=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = Profile.ROLE_OWNER
            profile.save()
        return user


class CatQuickForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ("name", "sex", "breed", "color", "birth_date")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }


class PassportQuickForm(forms.ModelForm):
    class Meta:
        model = HealthPassport
        fields = ("cat", "microchip_number", "blood_type", "sterilized", "weight_kg", "veterinarian_name", "clinic_phone")

    def __init__(self, *args, cat_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if cat_queryset is not None:
            self.fields["cat"].queryset = cat_queryset


class RecordQuickForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ("passport", "record_type", "title", "event_date", "next_due_date", "clinic", "doctor", "weight_kg", "description")
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "next_due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, passport_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if passport_queryset is not None:
            self.fields["passport"].queryset = passport_queryset

    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get("event_date")
        next_due_date = cleaned_data.get("next_due_date")
        if event_date and next_due_date and next_due_date < event_date:
            self.add_error("next_due_date", "Следующий срок не может быть раньше даты события.")
        return cleaned_data


class UserQuickForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", min_length=8, widget=forms.PasswordInput)
    role = forms.ChoiceField(label="Роль", choices=Profile.ROLE_CHOICES)
    phone = forms.CharField(label="Телефон", required=False)
    clinic = forms.CharField(label="Клиника", required=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data["role"]
            profile.phone = self.cleaned_data["phone"]
            profile.clinic = self.cleaned_data["clinic"]
            profile.save()
        return user
