import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITestCase(APITestCase):
    def setUp(self):
        # 1. Superuser / Owner
        self.owner = User.objects.create_superuser(
            username="owner_user",
            password="OwnerPassword123!",
            email="owner@example.com",
        )

        # 2. Editor
        self.editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor = User.objects.create_user(
            username="editor_user",
            password="EditorPassword123!",
            email="editor@example.com",
        )
        self.editor.groups.add(self.editor_group)

        # 3. Regular Authenticated User
        self.regular_user = User.objects.create_user(
            username="regular_user",
            password="RegularPassword123!",
            email="regular@example.com",
        )

        # Initial Experience entry
        self.experience = Experience.objects.create(
            title="Software Engineer Intern",
            description="Developing scalable web applications with Django and REST APIs.",
            category="internship",
            thumbnail="https://example.com/thumb.png",
        )

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", kwargs={"experience_id": self.experience.id})
        self.star_url = reverse("api:experience-star", kwargs={"experience_id": self.experience.id})

    # --- Role 1: Unauthenticated Visitor ---
    def test_visitor_can_read_list_and_detail(self):
        res_list = self.client.get(self.list_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

        res_detail = self.client.get(self.detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail.data["title"], "Software Engineer Intern")
        self.assertEqual(res_detail.data["category"], "internship")
        self.assertTrue(res_detail.data["is_ongoing"])

    def test_visitor_cannot_create_experience(self):
        initial_count = Experience.objects.count()
        payload = {
            "title": "Teaching Assistant",
            "description": "Grading assignments and mentoring students.",
            "category": "part-time",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), initial_count)

    def test_visitor_cannot_update_experience(self):
        res = self.client.patch(self.detail_url, {"title": "Hacked Experience"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Software Engineer Intern")

    def test_visitor_cannot_delete_experience(self):
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_visitor_cannot_star_experience(self):
        res = self.client.post(self.star_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

    # --- Role 2: Regular Authenticated User ---
    def test_regular_user_cannot_create_or_modify_or_delete_experience(self):
        self.client.force_authenticate(user=self.regular_user)

        # Create rejected
        initial_count = Experience.objects.count()
        res_create = self.client.post(self.list_url, {
            "title": "Volunteer at NGO",
            "description": "Helping community service programs.",
            "category": "volunteer",
        })
        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), initial_count)

        # Update rejected
        res_update = self.client.patch(self.detail_url, {"title": "Regular User Edit"})
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Software Engineer Intern")

        # Delete rejected
        res_delete = self.client.delete(self.detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_regular_user_can_star_and_unstar_experience(self):
        self.client.force_authenticate(user=self.regular_user)

        # Toggle star ON
        res_star = self.client.post(self.star_url)
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertEqual(res_star.data["star_count"], 1)
        self.assertTrue(res_star.data["is_starred"])
        self.assertIn(self.regular_user.username, res_star.data["starred_by_names"])
        self.assertTrue(self.experience.starred_by.filter(pk=self.regular_user.pk).exists())

        # Toggle star OFF
        res_unstar = self.client.post(self.star_url)
        self.assertEqual(res_unstar.status_code, status.HTTP_200_OK)
        self.assertEqual(res_unstar.data["star_count"], 0)
        self.assertFalse(res_unstar.data["is_starred"])
        self.assertFalse(self.experience.starred_by.filter(pk=self.regular_user.pk).exists())

    # --- Role 3: Editor ---
    def test_editor_cannot_create_experience(self):
        self.client.force_authenticate(user=self.editor)
        initial_count = Experience.objects.count()
        res = self.client.post(self.list_url, {
            "title": "Research Assistant",
            "description": "Analyzing machine learning datasets.",
            "category": "research",
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), initial_count)

    def test_editor_can_patch_experience(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.patch(self.detail_url, {"description": "Updated description by editor."})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.description, "Updated description by editor.")

    def test_editor_cannot_delete_experience(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    # --- Role 4: Superuser / Portfolio Owner ---
    def test_owner_can_create_update_and_delete_experience(self):
        self.client.force_authenticate(user=self.owner)

        # Create
        payload = {
            "title": "Backend Developer",
            "description": "Building microservices with Python and Go.",
            "category": "full-time",
            "thumbnail": "https://example.com/backend.png",
        }
        res_create = self.client.post(self.list_url, payload)
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        new_id = res_create.data["id"]
        self.assertTrue(Experience.objects.filter(pk=new_id).exists())

        # Update
        new_detail_url = reverse("api:experience-detail", kwargs={"experience_id": new_id})
        res_update = self.client.patch(new_detail_url, {"title": "Senior Backend Developer"})
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)
        self.assertEqual(Experience.objects.get(pk=new_id).title, "Senior Backend Developer")

        # Delete
        res_delete = self.client.delete(new_detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=new_id).exists())

    # --- Validation Tests ---
    def test_validation_xss_stripped(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "<b>Lead Architect</b>",
            "description": "<i>Design modern systems</i>",
            "category": "full-time",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Lead Architect")
        self.assertEqual(res.data["description"], "Design modern systems")

    def test_validation_empty_title_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "   ",
            "description": "Valid description",
            "category": "full-time",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", res.data)

    def test_validation_empty_description_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "Valid Title",
            "description": "   ",
            "category": "full-time",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", res.data)

    # --- Search Test ---
    def test_search_filters_experience(self):
        Experience.objects.create(
            title="UI/UX Designer",
            description="Designing mobile app user flows in Figma.",
            category="freelance",
        )
        Experience.objects.create(
            title="Data Analyst",
            description="Processing big data pipelines with SQL.",
            category="part-time",
        )

        # Search by title
        res = self.client.get(self.list_url, {"search": "Designer"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "UI/UX Designer")

        # Search by description
        res_desc = self.client.get(self.list_url, {"search": "pipelines"})
        self.assertEqual(res_desc.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_desc.data), 1)
        self.assertEqual(res_desc.data[0]["title"], "Data Analyst")

        # Search empty match
        res_empty = self.client.get(self.list_url, {"search": "NonExistentJobXYZ"})
        self.assertEqual(res_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_empty.data), 0)

    # --- CSRF Enforcement Test ---
    def test_csrf_enforced_for_session_auth(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        login_success = csrf_client.login(username="owner_user", password="OwnerPassword123!")
        self.assertTrue(login_success)

        # POST without CSRF token should return 403 Forbidden
        payload = {
            "title": "DevOps Engineer",
            "description": "Managing CI/CD and Kubernetes clusters.",
            "category": "full-time",
        }
        res = csrf_client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("CSRF", str(res.data.get("detail", "")))

