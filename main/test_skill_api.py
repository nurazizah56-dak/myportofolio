import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Skill


class SkillAPITestCase(APITestCase):
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

        # Initial Skill entry
        self.skill = Skill.objects.create(
            category="soft",
            name="Leadership",
            score=9.0,
            order=1,
        )

        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", kwargs={"skill_id": self.skill.id})
        self.star_url = reverse("api:skill-star", kwargs={"skill_id": self.skill.id})

    # --- Role 1: Unauthenticated Visitor ---
    def test_visitor_can_read_list_and_detail(self):
        res_list = self.client.get(self.list_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

        res_detail = self.client.get(self.detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail.data["name"], "Leadership")
        self.assertEqual(float(res_detail.data["score"]), 9.0)
        self.assertEqual(res_detail.data["percentage"], 90.0)

    def test_visitor_cannot_create_skill(self):
        initial_count = Skill.objects.count()
        payload = {"category": "hard", "name": "Python", "score": "8.5", "order": 2}
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skill.objects.count(), initial_count)

    def test_visitor_cannot_update_skill(self):
        res = self.client.patch(self.detail_url, {"name": "Hacked Skill"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Leadership")

    def test_visitor_cannot_delete_skill(self):
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_visitor_cannot_star_skill(self):
        res = self.client.post(self.star_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.skill.starred_by.count(), 0)

    # --- Role 2: Regular Authenticated User ---
    def test_regular_user_cannot_create_or_modify_or_delete_skill(self):
        self.client.force_authenticate(user=self.regular_user)

        # Create rejected
        initial_count = Skill.objects.count()
        res_create = self.client.post(self.list_url, {"category": "hard", "name": "Django", "score": "8.0", "order": 3})
        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skill.objects.count(), initial_count)

        # Update rejected
        res_update = self.client.patch(self.detail_url, {"name": "Regular User Edit"})
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Leadership")

        # Delete rejected
        res_delete = self.client.delete(self.detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_regular_user_can_star_and_unstar_skill(self):
        self.client.force_authenticate(user=self.regular_user)

        # Toggle star ON
        res_star = self.client.post(self.star_url)
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertEqual(res_star.data["star_count"], 1)
        self.assertTrue(res_star.data["is_starred"])
        self.assertIn(self.regular_user.username, res_star.data["starred_by_names"])
        self.assertTrue(self.skill.starred_by.filter(pk=self.regular_user.pk).exists())

        # Toggle star OFF
        res_unstar = self.client.post(self.star_url)
        self.assertEqual(res_unstar.status_code, status.HTTP_200_OK)
        self.assertEqual(res_unstar.data["star_count"], 0)
        self.assertFalse(res_unstar.data["is_starred"])
        self.assertFalse(self.skill.starred_by.filter(pk=self.regular_user.pk).exists())

    # --- Role 3: Editor ---
    def test_editor_cannot_create_skill(self):
        self.client.force_authenticate(user=self.editor)
        initial_count = Skill.objects.count()
        res = self.client.post(self.list_url, {"category": "hard", "name": "Docker", "score": "7.5", "order": 4})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skill.objects.count(), initial_count)

    def test_editor_can_patch_skill(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.patch(self.detail_url, {"score": "9.8"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(float(self.skill.score), 9.8)

    def test_editor_cannot_delete_skill(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())

    # --- Role 4: Superuser / Portfolio Owner ---
    def test_owner_can_create_update_and_delete_skill(self):
        self.client.force_authenticate(user=self.owner)

        # Create
        payload = {"category": "hard", "name": "TypeScript", "score": "8.8", "order": 5}
        res_create = self.client.post(self.list_url, payload)
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        new_id = res_create.data["id"]
        self.assertTrue(Skill.objects.filter(pk=new_id).exists())

        # Update
        new_detail_url = reverse("api:skill-detail", kwargs={"skill_id": new_id})
        res_update = self.client.patch(new_detail_url, {"score": "9.2"})
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)
        self.assertEqual(float(Skill.objects.get(pk=new_id).score), 9.2)

        # Delete
        res_delete = self.client.delete(new_detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Skill.objects.filter(pk=new_id).exists())

    # --- Validation Tests ---
    def test_validation_xss_stripped(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "category": "hard",
            "name": "<b>Golang</b>",
            "score": "8.0",
            "order": 1,
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], "Golang")

    def test_validation_empty_name_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {"category": "hard", "name": "   ", "score": "8.0", "order": 1}
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", res.data)

    def test_validation_invalid_score_rejected(self):
        self.client.force_authenticate(user=self.owner)
        # Score > 10
        res_high = self.client.post(self.list_url, {"category": "hard", "name": "Rust", "score": "15.0"})
        self.assertEqual(res_high.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("score", res_high.data)

        # Score < 0
        res_low = self.client.post(self.list_url, {"category": "hard", "name": "Rust", "score": "-2.0"})
        self.assertEqual(res_low.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("score", res_low.data)

    # --- Search Test ---
    def test_search_filters_skills(self):
        Skill.objects.create(category="hard", name="Python Programming", score=9.5, order=2)
        Skill.objects.create(category="soft", name="Public Speaking", score=8.0, order=3)

        # Search by name
        res = self.client.get(self.list_url, {"search": "Python"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Python Programming")

        # Search empty match
        res_empty = self.client.get(self.list_url, {"search": "NonExistentSkillXYZ"})
        self.assertEqual(res_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_empty.data), 0)

    # --- CSRF Enforcement Test ---
    def test_csrf_enforced_for_session_auth(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        login_success = csrf_client.login(username="owner_user", password="OwnerPassword123!")
        self.assertTrue(login_success)

        # POST without CSRF token should return 403 Forbidden
        payload = {"category": "hard", "name": "Kotlin", "score": "8.0", "order": 1}
        res = csrf_client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("CSRF", str(res.data.get("detail", "")))

