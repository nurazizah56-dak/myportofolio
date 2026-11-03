from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

from main.models import Experience, Education, Skill, Achievement, Certification


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Teaching Assistant for Business and Technical Communication (KOMBISTEK)",
            description="Assisted lecturers in evaluating assignments and mentoring students in professional communication.",
            category="part-time",
        )

        self.education = Education.objects.create(
            institution_name="Universitas Indonesia",
            degree="Bachelor of Information Systems",
            location="Depok, West Java",
            maps_url="https://maps.app.goo.gl/NcpBNCfPGqhKCqtk8",
            start_year=2025,
        )

        self.skill = Skill.objects.create(
            category="soft",
            name="Teamwork & Leadership",
            score=9.5,
        )

        self.achievement = Achievement.objects.create(
            title="Juara 1 Hackathon",
            description="Lomba Pemrograman Web",
            year=2025,
            category="academic",
        )

        self.achievement_with_image = Achievement.objects.create(
            title="Eagle Scout",
            description="Tambun Selatan District Scout Council",
            year=2024,
            category="non_academic",
            image="/static/images/scout_cert.png",
        )

        self.ukbi_cert = Certification.objects.create(
            title="Indonesian Language Proficiency Test (UKBI)",
            issuer="Agency for Language Development and Cultivation",
            date_range="July 2025 - July 2027",
            description='Achieved "Sangat Unggul" (Very Excellent) rating with a score of 688/800',
            icon="📜",
            image="/static/img/cert-ukbi.png",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), self.experience.title)
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience"')
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        json_response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertContains(json_response, self.experience.title)
        self.assertContains(json_response, self.experience.description)
        self.assertContains(json_response, "Part-Time")

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="empty"')
        json_response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertEqual(json_response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        self.assertFalse(self.experience.is_ongoing)
        json_response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(json_response.status_code, 200)
        data = json_response.json()
        self.assertFalse(data[0]["fields"]["is_ongoing"])

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_page_shows_data(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="education"')
        api_response = self.client.get(reverse("api:education-list"))
        self.assertEqual(api_response.status_code, 200)
        self.assertContains(api_response, self.education.institution_name)
        self.assertContains(api_response, self.education.degree)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="empty"')
        api_response = self.client.get(reverse("api:education-list"))
        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(api_response.json(), [])

    def test_education_is_ongoing(self):
        self.education.end_year = None
        self.education.save()
        self.assertTrue(self.education.is_ongoing)
        api_response = self.client.get(reverse("api:education-detail", kwargs={"education_id": self.education.id}))
        self.assertEqual(api_response.status_code, 200)
        self.assertTrue(api_response.data["is_ongoing"])

    def test_skills_page_is_accessible(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")

    def test_skills_page_shows_data(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="soft-skills-section"')
        json_response = self.client.get(reverse("main:get_skill_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertContains(json_response, self.skill.name)

    def test_empty_skills_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="skills-empty"')
        json_response = self.client.get(reverse("main:get_skill_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertEqual(json_response.json(), [])

    def test_achievements_page_is_accessible(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements.html")

    def test_achievements_page_shows_data(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="achievements"')
        json_response = self.client.get(reverse("main:get_achievement_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertContains(json_response, self.achievement.title)

    def test_achievement_category_separation(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="academic-section"')
        self.assertContains(response, 'id="non-academic-section"')
        json_response = self.client.get(reverse("main:get_achievement_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertContains(json_response, self.achievement.title)
        self.assertContains(json_response, self.achievement_with_image.title)

    def test_achievement_carousel_shows_only_items_with_image(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="carousel-section"')
        json_response = self.client.get(reverse("main:get_achievement_json"))
        self.assertEqual(json_response.status_code, 200)
        data = json_response.json()
        items_with_image = [item for item in data if item["fields"].get("image")]
        self.assertEqual(len(items_with_image), 1)
        self.assertEqual(items_with_image[0]["fields"]["image"], self.achievement_with_image.image)

    def test_empty_achievements_page(self):
        Achievement.objects.all().delete()
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="achievements-empty"')
        json_response = self.client.get(reverse("main:get_achievement_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertEqual(json_response.json(), [])

    def test_achievement_model_str(self):
        self.assertEqual(str(self.achievement), self.achievement.title)

    def test_certifications_url_and_template(self):
        response = self.client.get(reverse("main:show_certifications"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "certifications.html")

    def test_certifications_page_shows_data(self):
        response = self.client.get(reverse("main:show_certifications"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="cert-list"')
        json_response = self.client.get(reverse("main:get_certification_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertContains(json_response, "Indonesian Language Proficiency Test (UKBI)")

    def test_certifications_page_empty_state(self):
        Certification.objects.all().delete()
        response = self.client.get(reverse("main:show_certifications"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="certifications-empty"')
        json_response = self.client.get(reverse("main:get_certification_json"))
        self.assertEqual(json_response.status_code, 200)
        self.assertEqual(json_response.json(), [])
