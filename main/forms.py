from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateTimeInput, NumberInput

from main.models import Experience, Education


class ExperienceForm(ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Secret key"}),
        label="Secret Key",
        required=True,
    )

    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]
        labels = {
            "title": "Experience Title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail URL",
            "ended_at": "End Date (leave blank if ongoing)",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Software Engineer Intern", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Describe your experience", "rows": 3}),
            "category": Select(),
            "thumbnail": URLInput(attrs={"placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000"}),
            "ended_at": DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

class EducationForm(ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Kode rahasia"}),
        label="Kode Rahasia",
        required=True,
    )

    class Meta:
        model = Education
        fields = [
            "institution_name",
            "degree",
            "location",
            "maps_url",
            "logo",
            "start_year",
            "end_year",
        ]
        labels = {
            "institution_name": "Nama Institusi",
            "degree": "Gelar/Jenjang",
            "location": "Lokasi",
            "maps_url": "URL Google Maps",
            "logo": "URL Logo",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai (kosongkan jika masih berlangsung)",
        }
        widgets = {
            "institution_name": TextInput(attrs={"placeholder": "Universitas Indonesia"}),
            "degree": TextInput(attrs={"placeholder": "Bachelor of Information Systems"}),
            "location": TextInput(attrs={"placeholder": "Depok, Jawa Barat"}),
            "maps_url": URLInput(attrs={"placeholder": "https://maps.google.com/..."}),
            "logo": TextInput(attrs={"placeholder": "https://.../logo.png"}),
            "start_year": NumberInput(attrs={"placeholder": "2024"}),
            "end_year": NumberInput(attrs={"placeholder": "2028"}),
        }