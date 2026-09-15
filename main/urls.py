from django.urls import path

from main.views import (
    show_main, 
    show_experience, 
    create_experience,
    show_education, 
    show_skills, 
    show_achievements,
    show_certifications,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("education/", show_education, name="show_education"),
    path("skills/", show_skills, name="show_skills"),
    path("achievements/", show_achievements, name="show_achievements"),
    path("certifications/", show_certifications, name="show_certifications"),
]