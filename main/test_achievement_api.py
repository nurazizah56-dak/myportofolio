import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Achievement


class AchievementAPITestCase(APITestCase):
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

        # Initial Achievement entry
        self.achievement = Achievement.objects.create(
            title="Juara 1 Web Development",
            description="Lomba pengembangan website berskala nasional.",
            year=2025,
            category="academic",
            icon="🏆",
            image="/static/images/cert.png",
        )

        self.list_url = reverse("api:achievement-list")
        self.detail_url = reverse("api:achievement-detail", kwargs={"achievement_id": self.achievement.id})
        self.star_url = reverse("api:achievement-star", kwargs={"achievement_id": self.achievement.id})

    # --- Role 1: Unauthenticated Visitor ---
    def test_visitor_can_read_list_and_detail(self):
        res_list = self.client.get(self.list_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

        res_detail = self.client.get(self.detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail.data["title"], "Juara 1 Web Development")
        self.assertEqual(res_detail.data["year"], 2025)
        self.assertEqual(res_detail.data["category"], "academic")

    def test_visitor_cannot_create_achievement(self):
        initial_count = Achievement.objects.count()
        payload = {
            "title": "Eagle Scout",
            "description": "District Scout Council Award",
            "year": 2024,
            "category": "non_academic",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Achievement.objects.count(), initial_count)

    def test_visitor_cannot_update_achievement(self):
        res = self.client.patch(self.detail_url, {"title": "Hacked Title"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "Juara 1 Web Development")

    def test_visitor_cannot_delete_achievement(self):
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Achievement.objects.filter(pk=self.achievement.pk).exists())

    def test_visitor_cannot_star_achievement(self):
        res = self.client.post(self.star_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.achievement.starred_by.count(), 0)

    # --- Role 2: Regular Authenticated User ---
    def test_regular_user_cannot_create_or_modify_or_delete_achievement(self):
        self.client.force_authenticate(user=self.regular_user)

        # Create rejected
        initial_count = Achievement.objects.count()
        res_create = self.client.post(self.list_url, {
            "title": "Best Paper Award",
            "description": "Conference best paper",
            "year": 2026,
            "category": "academic",
        })
        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Achievement.objects.count(), initial_count)

        # Update rejected
        res_update = self.client.patch(self.detail_url, {"title": "Regular Edit"})
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "Juara 1 Web Development")

        # Delete rejected
        res_delete = self.client.delete(self.detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Achievement.objects.filter(pk=self.achievement.pk).exists())

    def test_regular_user_can_star_and_unstar_achievement(self):
        self.client.force_authenticate(user=self.regular_user)

        # Toggle star ON
        res_star = self.client.post(self.star_url)
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertEqual(res_star.data["star_count"], 1)
        self.assertTrue(res_star.data["is_starred"])
        self.assertIn(self.regular_user.username, res_star.data["starred_by_names"])
        self.assertTrue(self.achievement.starred_by.filter(pk=self.regular_user.pk).exists())

        # Toggle star OFF
        res_unstar = self.client.post(self.star_url)
        self.assertEqual(res_unstar.status_code, status.HTTP_200_OK)
        self.assertEqual(res_unstar.data["star_count"], 0)
        self.assertFalse(res_unstar.data["is_starred"])
        self.assertFalse(self.achievement.starred_by.filter(pk=self.regular_user.pk).exists())

    # --- Role 3: Editor ---
    def test_editor_cannot_create_achievement(self):
        self.client.force_authenticate(user=self.editor)
        initial_count = Achievement.objects.count()
        res = self.client.post(self.list_url, {
            "title": "Debate Champion",
            "description": "National English debate champion.",
            "year": 2025,
            "category": "academic",
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Achievement.objects.count(), initial_count)

    def test_editor_can_patch_achievement(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.patch(self.detail_url, {"year": 2026})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.year, 2026)

    def test_editor_cannot_delete_achievement(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Achievement.objects.filter(pk=self.achievement.pk).exists())

    # --- Role 4: Superuser / Portfolio Owner ---
    def test_owner_can_create_update_and_delete_achievement(self):
        self.client.force_authenticate(user=self.owner)

        # Create
        payload = {
            "title": "AI Innovation Challenge",
            "description": "Top 3 winner in national AI challenge.",
            "year": 2025,
            "category": "academic",
            "icon": "🥇",
            "image": "/static/images/ai-cert.png",
        }
        res_create = self.client.post(self.list_url, payload)
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        new_id = res_create.data["id"]
        self.assertTrue(Achievement.objects.filter(pk=new_id).exists())

        # Update
        new_detail_url = reverse("api:achievement-detail", kwargs={"achievement_id": new_id})
        res_update = self.client.patch(new_detail_url, {"title": "AI Innovation Winner"})
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)
        self.assertEqual(Achievement.objects.get(pk=new_id).title, "AI Innovation Winner")

        # Delete
        res_delete = self.client.delete(new_detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Achievement.objects.filter(pk=new_id).exists())

    # --- Validation Tests ---
    def test_validation_xss_stripped(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "<b>Gold Medalist</b>",
            "description": "<i>National Science Olympiad</i>",
            "year": 2024,
            "category": "academic",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Gold Medalist")
        self.assertEqual(res.data["description"], "National Science Olympiad")

    def test_validation_empty_title_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "   ",
            "description": "Valid description",
            "year": 2024,
            "category": "academic",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", res.data)

    def test_validation_empty_description_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "Valid Title",
            "description": "   ",
            "year": 2024,
            "category": "academic",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", res.data)

    def test_validation_invalid_year_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "Ancient Win",
            "description": "Too old",
            "year": 1800,
            "category": "academic",
        }
        res = self.client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("year", res.data)

    # --- Search Test ---
    def test_search_filters_achievements(self):
        Achievement.objects.create(
            title="Music Competition",
            description="Piano solo category winner.",
            year=2023,
            category="non_academic",
        )

        # Search by title
        res = self.client.get(self.list_url, {"search": "Music"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Music Competition")

        # Search by description
        res_desc = self.client.get(self.list_url, {"search": "Piano"})
        self.assertEqual(res_desc.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_desc.data), 1)
        self.assertEqual(res_desc.data[0]["title"], "Music Competition")

        # Search empty match
        res_empty = self.client.get(self.list_url, {"search": "NonExistentAchievementXYZ"})
        self.assertEqual(res_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_empty.data), 0)

    # --- CSRF Enforcement Test ---
    def test_csrf_enforced_for_session_auth(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        login_success = csrf_client.login(username="owner_user", password="OwnerPassword123!")
        self.assertTrue(login_success)

        # POST without CSRF token should return 403 Forbidden
        payload = {
            "title": "CSRF Test Win",
            "description": "Testing CSRF enforcement",
            "year": 2025,
            "category": "academic",
        }
        res = csrf_client.post(self.list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("CSRF", str(res.data.get("detail", "")))

