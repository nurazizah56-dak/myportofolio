import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education


class EducationAPITestCase(APITestCase):
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

        # Initial Education entry
        self.education = Education.objects.create(
            institution_name="Universitas Indonesia",
            degree="Bachelor of Information Systems",
            location="Depok, West Java",
            maps_url="https://maps.app.goo.gl/example",
            logo="https://example.com/ui-logo.png",
            start_year=2024,
            end_year=2028,
        )

        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", kwargs={"education_id": self.education.id})
        self.star_url = reverse("api:education-star", kwargs={"education_id": self.education.id})

    # --- Role 1: Unauthenticated Visitor ---
    def test_visitor_can_read_list_and_detail(self):
        res_list = self.client.get(self.list_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

        res_detail = self.client.get(self.detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail.data["institution_name"], "Universitas Indonesia")

    def test_visitor_cannot_create_education(self):
        payload = {
            "institution_name": "Institut Teknologi Bandung",
            "degree": "Informatics",
            "start_year": 2020,
        }
        res = self.client.post(self.list_url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_visitor_cannot_update_or_delete_education(self):
        patch_res = self.client.patch(self.detail_url, data={"degree": "Updated Degree"})
        self.assertEqual(patch_res.status_code, status.HTTP_403_FORBIDDEN)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "Bachelor of Information Systems")

        del_res = self.client.delete(self.detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Education.objects.filter(pk=self.education.id).exists())

    def test_visitor_cannot_star_education(self):
        res = self.client.post(self.star_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.education.starred_by.count(), 0)

    # --- Role 2: Regular Authenticated User ---
    def test_regular_user_cannot_create_update_or_delete(self):
        self.client.force_authenticate(user=self.regular_user)

        # Cannot create
        create_res = self.client.post(self.list_url, data={"institution_name": "ITB", "degree": "CS", "start_year": 2021})
        self.assertEqual(create_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

        # Cannot update
        patch_res = self.client.patch(self.detail_url, data={"degree": "Hacked"})
        self.assertEqual(patch_res.status_code, status.HTTP_403_FORBIDDEN)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "Bachelor of Information Systems")

        # Cannot delete
        del_res = self.client.delete(self.detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Education.objects.filter(pk=self.education.id).exists())

    def test_regular_user_can_toggle_star(self):
        self.client.force_authenticate(user=self.regular_user)

        # First star
        res1 = self.client.post(self.star_url)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res1.data["star_count"], 1)
        self.assertTrue(res1.data["is_starred"])
        self.assertEqual(self.education.starred_by.count(), 1)

        # Second star (toggle off)
        res2 = self.client.post(self.star_url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["star_count"], 0)
        self.assertFalse(res2.data["is_starred"])
        self.assertEqual(self.education.starred_by.count(), 0)

    # --- Role 3: Editor ---
    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        # Editor cannot create
        create_res = self.client.post(self.list_url, data={"institution_name": "UGM", "degree": "CS", "start_year": 2022})
        self.assertEqual(create_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

        # Editor cannot delete
        del_res = self.client.delete(self.detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Education.objects.filter(pk=self.education.id).exists())

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)

        # PATCH
        patch_res = self.client.patch(self.detail_url, data={"degree": "B.Sc. in Information Systems"})
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "B.Sc. in Information Systems")

        # PUT
        put_payload = {
            "institution_name": "Universitas Indonesia (Fasilkom)",
            "degree": "B.Sc. in Information Systems",
            "location": "Depok",
            "start_year": 2024,
            "end_year": 2028,
        }
        put_res = self.client.put(self.detail_url, data=put_payload)
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "Universitas Indonesia (Fasilkom)")

    # --- Role 4: Portfolio Owner (Superuser) ---
    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        # Create
        new_payload = {
            "institution_name": "SMA Negeri 1 Jakarta",
            "degree": "Natural Sciences",
            "location": "Jakarta",
            "start_year": 2021,
            "end_year": 2024,
        }
        create_res = self.client.post(self.list_url, data=new_payload)
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.count(), 2)

        created_id = create_res.data["id"]

        # Delete
        del_url = reverse("api:education-detail", kwargs={"education_id": created_id})
        del_res = self.client.delete(del_url)
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Education.objects.count(), 1)

    # --- Input Validation & XSS ---
    def test_validation_empty_institution_name(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "institution_name": "   ",
            "degree": "Information Systems",
            "start_year": 2024,
        }
        res = self.client.post(self.list_url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("institution_name", res.data)

    def test_validation_xss_stripped(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "institution_name": "<b>Harvard University</b>",
            "degree": "<b>Computer Science</b>",
            "location": "<i>Cambridge</i>",
            "start_year": 2025,
        }
        res = self.client.post(self.list_url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["institution_name"], "Harvard University")
        self.assertEqual(res.data["degree"], "Computer Science")
        self.assertEqual(res.data["location"], "Cambridge")

    def test_validation_html_only_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "institution_name": "<h1>   </h1>",
            "degree": "Computer Science",
            "start_year": 2025,
        }
        res = self.client.post(self.list_url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("institution_name", res.data)

    def test_validation_invalid_year_range(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "institution_name": "MIT",
            "degree": "AI",
            "start_year": 2025,
            "end_year": 2020,  # end_year before start_year!
        }
        res = self.client.post(self.list_url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("end_year", res.data)

    # --- Query Params Search ---
    def test_search_education(self):
        Education.objects.create(
            institution_name="Institut Teknologi Bandung",
            degree="Informatics",
            location="Bandung",
            start_year=2020,
        )
        res = self.client.get(f"{self.list_url}?search=Bandung")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["institution_name"], "Institut Teknologi Bandung")

    # --- CSRF Enforcement Test ---
    def test_csrf_protection_enforced(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        logged_in = csrf_client.login(username="owner_user", password="OwnerPassword123!")
        self.assertTrue(logged_in)

        # POST without CSRF token must return 403 Forbidden
        no_csrf_res = csrf_client.post(self.list_url, data={
            "institution_name": "Stanford",
            "degree": "Data Science",
            "start_year": 2024,
        })
        self.assertEqual(no_csrf_res.status_code, status.HTTP_403_FORBIDDEN)
