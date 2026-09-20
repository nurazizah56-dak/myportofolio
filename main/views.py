from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.http import JsonResponse

from main.forms import ExperienceForm, EducationForm
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

def add_experience(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Validasi password/secret key
        if password != 'PASSWORD_KAMU':
            messages.error(request, 'Wrong password 🤷‍♂️!')
            return redirect('main:show_experience')

        # Jika sukses
        messages.success(request, 'Experience successfully added! 🎉')
        return redirect('main:show_experience')

    return render(request, 'experience.html')

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