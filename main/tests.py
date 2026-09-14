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
            category="academic"
        )

        self.achievement_with_image = Achievement.objects.create(
            title="Eagle Scout",
            description="Tambun Selatan District Scout Council",
            year=2024,
            category="non_academic",
            image="/static/images/scout_cert.png"
        )

        self.ukbi_cert = Certification.objects.create(
        title='Indonesian Language Proficiency Test (UKBI)',
        issuer='Agency for Language Development and Cultivation',
        date_range='July 2025 - July 2027',
        description='Achieved "Sangat Unggul" (Very Excellent) rating with a score of 688/800',
        icon='📜',
        image='/static/img/cert-ukbi.png',
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
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_page_shows_data(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, self.education.institution_name)
        self.assertContains(response, self.education.degree)
        self.assertContains(response, self.education.location)

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "Belum ada riwayat pendidikan yang ditambahkan.")

    def test_education_is_ongoing(self):
        self.assertTrue(self.education.is_ongoing)
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "Present")

    def test_skills_page_is_accessible(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")

    def test_skills_page_shows_data(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertContains(response, self.skill.name, html=True)
        self.assertContains(response, str(self.skill.score))

    def test_empty_skills_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))
        self.assertContains(response, "Belum ada soft skill yang ditambahkan.")

    def test_achievements_page_is_accessible(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements.html")

    def test_achievements_page_shows_data(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertContains(response, escape(self.achievement.title))
        self.assertContains(response, escape(self.achievement.description))
        self.assertContains(response, str(self.achievement.year))

    def test_achievement_category_separation(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertContains(response, escape(self.achievement.title))
        self.assertContains(response, escape(self.achievement_with_image.title))

    def test_achievement_carousel_shows_only_items_with_image(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertContains(response, self.achievement_with_image.image)

    def test_empty_achievements_page(self):
        Achievement.objects.all().delete()
        response = self.client.get(reverse("main:show_achievements"))
        self.assertContains(response, "Belum ada pencapaian akademik.")
        self.assertContains(response, "Belum ada pencapaian non-akademik.")

    def test_achievement_model_str(self):
        self.assertEqual(str(self.achievement), self.achievement.title)

    def test_certifications_url_and_template(self):
        response = self.client.get(reverse("main:show_certifications"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "certifications.html")

    def test_certifications_page_shows_data(self):
        response = self.client.get(reverse("main:show_certifications"))
        self.assertContains(response, "Indonesian Language Proficiency Test (UKBI)")
        self.assertContains(response, "Agency for Language Development and Cultivation")

    def test_certifications_page_empty_state(self):
        Certification.objects.all().delete()
        response = self.client.get(reverse("main:show_certifications"))
        self.assertContains(response, "Belum ada sertifikasi yang ditambahkan.")