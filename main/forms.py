from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateTimeInput, NumberInput

from main.models import Experience, Education, Skill, Achievement, Certification


class ExperienceForm(ModelForm):
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

    def clean_title(self):
        from django.utils.html import strip_tags
        from django.core.exceptions import ValidationError
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Experience title cannot be empty or contain only HTML tags.")
        return title

    def clean_description(self):
        from django.utils.html import strip_tags
        return strip_tags(self.cleaned_data["description"]).strip()

    def clean_category(self):
        from django.utils.html import strip_tags
        return strip_tags(self.cleaned_data["category"]).strip()

class EducationForm(ModelForm):
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
            "institution_name": "Institution Name",
            "degree": "Degree",
            "location": "Location",
            "maps_url": "Google Maps URL",
            "logo": "Logo URL",
            "start_year": "Start Year",
            "end_year": "End Year (leave blank if ongoing)",
        }
        widgets = {
            "institution_name": TextInput(attrs={"placeholder": "Universitas Indonesia"}),
            "degree": TextInput(attrs={"placeholder": "Bachelor of Information Systems"}),
            "location": TextInput(attrs={"placeholder": "Depok, West Java"}),
            "maps_url": URLInput(attrs={"placeholder": "https://maps.google.com/..."}),
            "logo": TextInput(attrs={"placeholder": "https://.../logo.png"}),
            "start_year": NumberInput(attrs={"placeholder": "2024"}),
            "end_year": NumberInput(attrs={"placeholder": "2028"}),
        }

    def clean_institution_name(self):
        from django.utils.html import strip_tags
        from django.core.exceptions import ValidationError
        institution_name = strip_tags(self.cleaned_data["institution_name"]).strip()
        if not institution_name:
            raise ValidationError("Institution name cannot be empty or contain only HTML tags.")
        return institution_name

    def clean_degree(self):
        from django.utils.html import strip_tags
        return strip_tags(self.cleaned_data["degree"]).strip()

    def clean_location(self):
        from django.utils.html import strip_tags
        return strip_tags(self.cleaned_data["location"]).strip()


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "category",
            "name",
            "score",
            "order",
        ]
        labels = {
            "category": "Category",
            "name": "Skill Name",
            "score": "Score (0-10)",
            "order": "Display Order",
        }
        widgets = {
            "category": Select(),
            "name": TextInput(attrs={"placeholder": "Python"}),
            "score": NumberInput(attrs={"placeholder": "8.5", "step": "0.1", "min": "0", "max": "10"}),
            "order": NumberInput(attrs={"placeholder": "1"}),
        }

    def clean_name(self):
        from django.utils.html import strip_tags
        from django.core.exceptions import ValidationError
        name = strip_tags(self.cleaned_data["name"]).strip()
        if not name:
            raise ValidationError("Skill name cannot be empty or contain only HTML tags.")
        return name

class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = [
            "title",
            "description",
            "year",
            "category",
            "icon",
            "image",
        ]
        labels = {
            "title": "Title",
            "description": "Description",
            "year": "Year",
            "category": "Category",
            "icon": "Icon (emoji)",
            "image": "Image filename (in static/img/)",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "1st Place National Debate Competition"}),
            "description": Textarea(attrs={"placeholder": "Describe the achievement", "rows": 3}),
            "year": NumberInput(attrs={"placeholder": "2026"}),
            "category": Select(),
            "icon": TextInput(attrs={"placeholder": "🏆"}),
            "image": TextInput(attrs={"placeholder": "/static/img/achievement-example.jpg"}),
        }

class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = [
            "title",
            "issuer",
            "date_range",
            "description",
            "icon",
            "image",
        ]
        labels = {
            "title": "Title",
            "issuer": "Issuer",
            "date_range": "Date Range",
            "description": "Description",
            "icon": "Icon (emoji)",
            "image": "Image path",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Python Programming Certificate"}),
            "issuer": TextInput(attrs={"placeholder": "Dicoding Indonesia"}),
            "date_range": TextInput(attrs={"placeholder": "July 2025 - July 2027"}),
            "description": Textarea(attrs={"placeholder": "Short description (optional)", "rows": 3}),
            "icon": TextInput(attrs={"placeholder": "📜"}),
            "image": TextInput(attrs={"placeholder": "/static/img/cert-example.png"}),
        }