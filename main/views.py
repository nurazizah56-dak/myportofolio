from django.shortcuts import render

from main.models import Experience


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