from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ExperienceForm
from main.models import Experience, Education, Skill, Achievement, Certification


def show_main(request):
    context = {
        "name": "Nur Azizah",
        "npm": "2506547935",
        "study_program": "Bachelor of Information Systems",
        "bio": (
            "Information Systems student at Universitas Indonesia bridging the gap between business needs and technical solutions. "
            "Proven track record of managing tight timelines and diverse stakeholder expectations through student organizations, "
            "academic projects, and teaching assistantships."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Nur Azizah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Nur Azizah",
        "education_list": Education.objects.all().order_by('-start_year'),
    }
    return render(request, "education.html", context)

def show_skills(request):
    context = {
        "name": "Nur Azizah",
        "soft_skills": Skill.objects.filter(category='soft'),
        "hard_skills": Skill.objects.filter(category='hard'),
    }
    return render(request, "skills.html", context)

def show_achievements(request):
    context = {
        "name": "Nur Azizah",
        "academic_achievements": Achievement.objects.filter(category='academic').order_by('-year'),
        "non_academic_achievements": Achievement.objects.filter(category='non_academic').order_by('-year'),
        "carousel_items": Achievement.objects.exclude(image__isnull=True).exclude(image__exact=''),
    }
    return render(request, "achievements.html", context)

def show_certifications(request):
    context = {
        "name": "Nur Azizah",
        "certification_list": Certification.objects.all(),
    }
    return render(request, "certifications.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def get_experience_json(request):
    category_query = request.GET.get("category", "").strip()
    experiences = Experience.objects.all()

    if category_query:
        experiences = experiences.filter(category__icontains=category_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")