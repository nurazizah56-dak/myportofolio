from django.shortcuts import render

from main.models import Experience, Education, Skill, Achievement


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