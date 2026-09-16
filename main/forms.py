from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateTimeInput

from main.models import Experience


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