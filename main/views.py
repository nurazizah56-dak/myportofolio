from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.http import JsonResponse

from main.forms import ExperienceForm, EducationForm, SkillForm, AchievementForm, CertificationForm
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
    json_response = get_experience_json(request)
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]

    category_query = request.GET.get("category", "").strip()

    context = {
        "name": "Nur Azizah",
        "experience_list": experiences,
        "category_query": category_query,
    }
    return render(request, "experience.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_experience")

        experience = form.save(commit=False)
        experience.save()
        messages.success(request, "New experience added successfully!")
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

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        password = request.POST.get("password", "")
        if password != settings.SECRET_PORTFOLIO_KEY:
            return JsonResponse({"success": False, "message": "Incorrect secret key"}, status=403)

        experience.delete()
        return JsonResponse({"success": True, "message": "Experience deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


def show_education(request):
    json_response = get_education_json(request)
    education_list = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [e.object for e in education_list]

    context = {
        "name": "Nur Azizah",
        "education_list": education_list,
    }
    return render(request, "education.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_education")

        education = form.save(commit=False)
        education.save()
        messages.success(request, "Education added successfully!")
        return redirect("main:show_education")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "education_form.html", context)

def get_education_json(request):
    education = Education.objects.all().order_by('-start_year')
    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")

def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_education")

        form.save()
        messages.success(request, "Education updated successfully!")
        return redirect("main:show_education")

    context = {
        "name": "Nur Azizah",
        "form": form,
        "education": education,
    }
    return render(request, "education_form.html", context)

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        password = request.POST.get("password", "")
        if password != settings.SECRET_PORTFOLIO_KEY:
            return JsonResponse({"success": False, "message": "Incorrect secret key"}, status=403)

        education.delete()
        return JsonResponse({"success": True, "message": "Education deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


def show_skills(request):
    json_response = get_skill_json(request)
    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [s.object for s in skills]

    soft_skills = [s for s in skills if s.category == "soft"]
    hard_skills = [s for s in skills if s.category == "hard"]

    context = {
        "name": "Nur Azizah",
        "soft_skills": soft_skills,
        "hard_skills": hard_skills,
    }
    return render(request, "skills.html", context)

def get_skill_json(request):
    skills = Skill.objects.all()
    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def create_skill(request):
    form = SkillForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_skills")

        skill = form.save(commit=False)
        skill.save()
        messages.success(request, "Skill added successfully!")
        return redirect("main:show_skills")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "skill_form.html", context)

def update_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_skills")

        form.save()
        messages.success(request, "Skill updated successfully!")
        return redirect("main:show_skills")

    context = {
        "name": "Nur Azizah",
        "form": form,
        "skill": skill,
    }
    return render(request, "skill_form.html", context)

def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        password = request.POST.get("password", "")
        if password != settings.SECRET_PORTFOLIO_KEY:
            return JsonResponse({"success": False, "message": "Incorrect secret key"}, status=403)

        skill.delete()
        return JsonResponse({"success": True, "message": "Skill deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


def show_achievements(request):
    json_response = get_achievement_json(request)
    achievements = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    achievements = [a.object for a in achievements]

    academic_achievements = sorted(
        [a for a in achievements if a.category == "academic"],
        key=lambda a: a.year, reverse=True
    )
    non_academic_achievements = sorted(
        [a for a in achievements if a.category == "non_academic"],
        key=lambda a: a.year, reverse=True
    )
    carousel_items = [a for a in achievements if a.image]

    context = {
        "name": "Nur Azizah",
        "academic_achievements": academic_achievements,
        "non_academic_achievements": non_academic_achievements,
        "carousel_items": carousel_items,
    }
    return render(request, "achievements.html", context)

def get_achievement_json(request):
    achievements = Achievement.objects.all()
    achievements_json = serializers.serialize("json", achievements)
    return HttpResponse(achievements_json, content_type="application/json")

def create_achievement(request):
    form = AchievementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_achievements")

        achievement = form.save(commit=False)
        achievement.save()
        messages.success(request, "Achievement added successfully!")
        return redirect("main:show_achievements")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "achievement_form.html", context)

def update_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    form = AchievementForm(request.POST or None, instance=achievement)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_achievements")

        form.save()
        messages.success(request, "Achievement updated successfully!")
        return redirect("main:show_achievements")

    context = {
        "name": "Nur Azizah",
        "form": form,
        "achievement": achievement,
    }
    return render(request, "achievement_form.html", context)

def delete_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        password = request.POST.get("password", "")
        if password != settings.SECRET_PORTFOLIO_KEY:
            return JsonResponse({"success": False, "message": "Incorrect secret key"}, status=403)

        achievement.delete()
        return JsonResponse({"success": True, "message": "Achievement deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


def show_certifications(request):
    json_response = get_certification_json(request)
    certifications = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    certification_list = sorted([c.object for c in certifications], key=lambda c: c.title)

    context = {
        "name": "Nur Azizah",
        "certification_list": certification_list,
    }
    return render(request, "certifications.html", context)

def get_certification_json(request):
    certifications = Certification.objects.all()
    certifications_json = serializers.serialize("json", certifications)
    return HttpResponse(certifications_json, content_type="application/json")

def create_certification(request):
    form = CertificationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_certifications")

        certification = form.save(commit=False)
        certification.save()
        messages.success(request, "Certification added successfully!")
        return redirect("main:show_certifications")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "certification_form.html", context)

def update_certification(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)
    form = CertificationForm(request.POST or None, instance=certification)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["password"] != settings.SECRET_PORTFOLIO_KEY:
            messages.error(request, "Incorrect secret key!")
            return redirect("main:show_certifications")

        form.save()
        messages.success(request, "Certification updated successfully!")
        return redirect("main:show_certifications")

    context = {
        "name": "Nur Azizah",
        "form": form,
        "certification": certification,
    }
    return render(request, "certification_form.html", context)

def delete_certification(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)

    if request.method == "POST":
        password = request.POST.get("password", "")
        if password != settings.SECRET_PORTFOLIO_KEY:
            return JsonResponse({"success": False, "message": "Incorrect secret key"}, status=403)

        certification.delete()
        return JsonResponse({"success": True, "message": "Certification deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)