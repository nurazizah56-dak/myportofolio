from django.urls import path

from main.views import (
    show_main, 
    show_experience, 
    create_experience,
    get_experience_json,
    delete_experience,
    show_education, 
    create_education,
    update_education,
    delete_education,
    get_education_json,
    show_skills, 
    show_achievements,
    show_certifications,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/<uuid:education_id>/edit/", update_education, name="update_education"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("skills/", show_skills, name="show_skills"),
    path("achievements/", show_achievements, name="show_achievements"),
    path("certifications/", show_certifications, name="show_certifications"),
]