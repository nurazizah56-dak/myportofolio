import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    maps_url = models.URLField(blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.institution_name

    @property
    def is_ongoing(self):
        return self.end_year is None


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('soft', 'Soft Skill'),
        ('hard', 'Hard Skill'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='soft')
    name = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=3, decimal_places=1, default=0)  # 0.0 - 10.0
    order = models.PositiveIntegerField(default=0, help_text="Urutan tampil, angka kecil duluan")

    class Meta:
        ordering = ['category', 'order', '-score']

    def __str__(self):
        return f"{self.name} ({self.score})"

    @property
    def percentage(self):
        return float(self.score) * 10


