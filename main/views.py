from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from main.forms import ExperienceForm, EducationForm, SkillForm, AchievementForm, CertificationForm
from main.models import Experience, Education, Skill, Achievement, Certification

import datetime

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No login session / Cookie not found')
    context = {
        "name": "Nur Azizah",
        "npm": "2506547935",
        "study_program": "Bachelor of Information Systems",
        "bio": (
            "Information Systems student at Universitas Indonesia bridging the gap between business needs and technical solutions. "
            "Proven track record of managing tight timelines and diverse stakeholder expectations through student organizations, "
            "academic projects, and teaching assistantships."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)



from django.views.decorators.http import require_POST

def show_experience(request):
    category_query = request.GET.get("category", "").strip()
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Nur Azizah",
        "category_query": category_query,
        "title_query": title_query,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        experience = form.save(commit=False)
        experience.save()
        messages.success(request, "New experience added successfully!")
        return redirect("main:show_experience")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "experience_form.html", context)


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add an experience."},
            status=403,
        )
    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience added successfully.", "pk": str(experience.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


def get_experience_json(request):
    category_query = request.GET.get("category", "").strip()
    title_query = request.GET.get("title", "").strip()

    experiences = Experience.objects.prefetch_related('starred_by').all()

    if category_query:
        experiences = experiences.filter(category__icontains=category_query)
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for exp in experiences:
        starred_users = exp.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])
        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "description": exp.description,
                "category": exp.category,
                "category_display": exp.get_category_display(),
                "thumbnail": exp.thumbnail,
                "is_ongoing": exp.is_ongoing,
                "ended_at": exp.ended_at.strftime("%Y-%m-%d %H:%M") if exp.ended_at else None,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience updated successfully!")
        return redirect("main:show_experience")

    context = {
        "name": "Nur Azizah",
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        return JsonResponse({"success": True, "message": "Experience deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)
        return redirect("main:show_experience")
    return redirect("main:show_experience")



def show_education(request):
    json_response = get_education_json(request)
    education_list = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [e.object for e in education_list]

    is_editor = request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Nur Azizah",
        "education_list": education_list,
        "is_editor": is_editor,
    }
    return render(request, "education.html", context)


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
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
    education_json = serializers.serialize("json", education, use_natural_foreign_keys=True)
    return HttpResponse(education_json, content_type="application/json")


@login_required(login_url="/login/")
def update_education(request, education_id):
    is_editor = request.user.groups.filter(name="Editor").exists()
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education updated successfully!")
        return redirect("main:show_education")

    context = {
        "name": "Nur Azizah",
        "form": form,
        "education": education,
    }
    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        return JsonResponse({"success": True, "message": "Education deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


@login_required(login_url="/login/")
def toggle_star_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)
        return redirect("main:show_education")
    return redirect("main:show_education")



def show_skills(request):
    json_response = get_skill_json(request)
    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [s.object for s in skills]
    soft_skills = [s for s in skills if s.category == "soft"]
    hard_skills = [s for s in skills if s.category == "hard"]
    is_editor = request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()
    context = {
        "name": "Nur Azizah",
        "soft_skills": soft_skills,
        "hard_skills": hard_skills,
        "is_editor": is_editor,
    }
    return render(request, "skills.html", context)


def get_skill_json(request):
    skills = Skill.objects.all()
    skills_json = serializers.serialize("json", skills, use_natural_foreign_keys=True)
    return HttpResponse(skills_json, content_type="application/json")


@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = SkillForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        skill = form.save(commit=False)
        skill.save()
        messages.success(request, "Skill added successfully!")
        return redirect("main:show_skills")
    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "skill_form.html", context)


@login_required(login_url="/login/")
def update_skill(request, skill_id):
    is_editor = request.user.groups.filter(name="Editor").exists()
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill updated successfully!")
        return redirect("main:show_skills")
    context = {
        "name": "Nur Azizah",
        "form": form,
        "skill": skill,
    }
    return render(request, "skill_form.html", context)


@login_required(login_url="/login/")
def delete_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=skill_id)
    if request.method == "POST":
        skill.delete()
        return JsonResponse({"success": True, "message": "Skill deleted successfully"})
    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


@login_required(login_url="/login/")
def toggle_star_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if request.method == "POST":
        if request.user in skill.starred_by.all():
            skill.starred_by.remove(request.user)
        else:
            skill.starred_by.add(request.user)
        return redirect("main:show_skills")
    return redirect("main:show_skills")



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

    is_editor = request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Nur Azizah",
        "academic_achievements": academic_achievements,
        "non_academic_achievements": non_academic_achievements,
        "carousel_items": carousel_items,
        "is_editor": is_editor,
    }
    return render(request, "achievements.html", context)


def get_achievement_json(request):
    achievements = Achievement.objects.all()
    achievements_json = serializers.serialize("json", achievements, use_natural_foreign_keys=True)
    return HttpResponse(achievements_json, content_type="application/json")


@login_required(login_url="/login/")
def create_achievement(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = AchievementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        achievement = form.save(commit=False)
        achievement.save()
        messages.success(request, "Achievement added successfully!")
        return redirect("main:show_achievements")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "achievement_form.html", context)


@login_required(login_url="/login/")
def update_achievement(request, achievement_id):
    is_editor = request.user.groups.filter(name="Editor").exists()
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied

    achievement = get_object_or_404(Achievement, pk=achievement_id)
    form = AchievementForm(request.POST or None, instance=achievement)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Achievement updated successfully!")
        return redirect("main:show_achievements")

    context = {
        "name": "Nur Azizah",
        "form": form,
        "achievement": achievement,
    }
    return render(request, "achievement_form.html", context)


@login_required(login_url="/login/")
def delete_achievement(request, achievement_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        achievement.delete()
        return JsonResponse({"success": True, "message": "Achievement deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


@login_required(login_url="/login/")
def toggle_star_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    if request.method == "POST":
        if request.user in achievement.starred_by.all():
            achievement.starred_by.remove(request.user)
        else:
            achievement.starred_by.add(request.user)
        return redirect("main:show_achievements")
    return redirect("main:show_achievements")



def show_certifications(request):
    json_response = get_certification_json(request)
    certifications = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    certification_list = sorted([c.object for c in certifications], key=lambda c: c.title)

    is_editor = request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Nur Azizah",
        "certification_list": certification_list,
        "is_editor": is_editor,
    }
    return render(request, "certifications.html", context)


def get_certification_json(request):
    certifications = Certification.objects.all()
    certifications_json = serializers.serialize("json", certifications, use_natural_foreign_keys=True)
    return HttpResponse(certifications_json, content_type="application/json")


@login_required(login_url="/login/")
def create_certification(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = CertificationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        certification = form.save(commit=False)
        certification.save()
        messages.success(request, "Certification added successfully!")
        return redirect("main:show_certifications")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "certification_form.html", context)


@login_required(login_url="/login/")
def update_certification(request, certification_id):
    is_editor = request.user.groups.filter(name="Editor").exists()
    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied

    certification = get_object_or_404(Certification, pk=certification_id)
    form = CertificationForm(request.POST or None, instance=certification)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Certification updated successfully!")
        return redirect("main:show_certifications")

    context = {
        "name": "Nur Azizah",
        "form": form,
        "certification": certification,
    }
    return render(request, "certification_form.html", context)


@login_required(login_url="/login/")
def delete_certification(request, certification_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    certification = get_object_or_404(Certification, pk=certification_id)

    if request.method == "POST":
        certification.delete()
        return JsonResponse({"success": True, "message": "Certification deleted successfully"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=405)


@login_required(login_url="/login/")
def toggle_star_certification(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)
    if request.method == "POST":
        if request.user in certification.starred_by.all():
            certification.starred_by.remove(request.user)
        else:
            certification.starred_by.add(request.user)
        return redirect("main:show_certifications")
    return redirect("main:show_certifications")



def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect("main:login")

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Nur Azizah",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response