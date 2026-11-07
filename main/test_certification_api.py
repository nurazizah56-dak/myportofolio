import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Certification


class CertificationAPITestCase(APITestCase):
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

        # Initial Certification entry
        self.certification = Certification.objects.create(
            title="AWS Certified Cloud Practitioner",
            issuer="Amazon Web Services",
            date_range="Jan 2025 - Jan 2028",
            description="Foundational understanding of AWS Cloud concepts.",
            icon="📜",
            image="/static/img/cert.png",
        )

        self.list_url = reverse("api:certification-list")
        self.detail_url = reverse("api:certification-detail", kwargs={"certification_id": self.certification.id})
        self.star_url = reverse("api:certification-star", kwargs={"certification_id": self.certification.id})

    # --- Role 1: Unauthenticated Visitor ---
    def test_visitor_can_read_list_and_detail(self):
        res_list = self.client.get(self.list_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

        res_detail = self.client.get(self.detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail.data["title"], "AWS Certified Cloud Practitioner")
        self.assertEqual(res_detail.data["issuer"], "Amazon Web Services")

    def test_visitor_cannot_create_certification(self):
        payload = {
            "title": "Google Cloud Associate Engineer",
            "issuer": "Google",
            "date_range": "2025 - 2028",
            "description": "Cloud certification",
            "icon": "📜",
            "image": "",
        }
        res = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_visitor_cannot_update_certification(self):
        res = self.client.patch(self.detail_url, {"title": "Hacked Title"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_visitor_cannot_delete_certification(self):
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_visitor_cannot_star_certification(self):
        res = self.client.post(self.star_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # --- Role 2: Regular Authenticated User ---
    def test_regular_user_cannot_create_or_modify_or_delete_certification(self):
        self.client.force_authenticate(user=self.regular_user)

        # Cannot create
        payload = {
            "title": "Certified Kubernetes Administrator",
            "issuer": "CNCF",
            "date_range": "2025 - 2028",
            "description": "K8s certification",
            "icon": "📜",
            "image": "",
        }
        res_create = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)

        # Cannot update
        res_update = self.client.patch(self.detail_url, {"title": "Updated Title"}, format="json")
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)

        # Cannot delete
        res_delete = self.client.delete(self.detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_can_star_and_unstar_certification(self):
        self.client.force_authenticate(user=self.regular_user)

        # 1. Star
        res_star = self.client.post(self.star_url)
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertEqual(res_star.data["star_count"], 1)
        self.assertTrue(res_star.data["is_starred"])
        self.assertIn("regular_user", res_star.data["starred_by_names"])

        # 2. Unstar
        res_unstar = self.client.post(self.star_url)
        self.assertEqual(res_unstar.status_code, status.HTTP_200_OK)
        self.assertEqual(res_unstar.data["star_count"], 0)
        self.assertFalse(res_unstar.data["is_starred"])
        self.assertEqual(res_unstar.data["starred_by_names"], "")

    # --- Role 3: Editor ---
    def test_editor_cannot_create_certification(self):
        self.client.force_authenticate(user=self.editor)
        payload = {
            "title": "HashiCorp Certified Terraform Associate",
            "issuer": "HashiCorp",
            "date_range": "2025 - 2027",
            "description": "IaC certification",
            "icon": "📜",
            "image": "",
        }
        res = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_patch_certification(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.patch(
            self.detail_url,
            {"description": "Updated certification description by editor."},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["description"], "Updated certification description by editor.")

    def test_editor_cannot_delete_certification(self):
        self.client.force_authenticate(user=self.editor)
        res = self.client.delete(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # --- Role 4: Portfolio Owner (Superuser) ---
    def test_owner_can_create_update_and_delete_certification(self):
        self.client.force_authenticate(user=self.owner)

        # 1. Create
        payload = {
            "title": "Meta Certified Front-End Developer",
            "issuer": "Meta",
            "date_range": "2025 - 2027",
            "description": "Comprehensive frontend certification",
            "icon": "💻",
            "image": "/static/img/meta.png",
        }
        res_create = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        new_cert_id = res_create.data["id"]

        # 2. Update (PUT)
        new_detail_url = reverse("api:certification-detail", kwargs={"certification_id": new_cert_id})
        update_payload = {
            "title": "Meta Certified Front-End Developer Professional",
            "issuer": "Meta / Coursera",
            "date_range": "2025 - 2028",
            "description": "Updated description",
            "icon": "💻",
            "image": "/static/img/meta.png",
        }
        res_update = self.client.put(new_detail_url, update_payload, format="json")
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)
        self.assertEqual(res_update.data["title"], "Meta Certified Front-End Developer Professional")

        # 3. Delete
        res_delete = self.client.delete(new_detail_url)
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Certification.objects.filter(pk=new_cert_id).exists())

    # --- Sanitization & Validation Tests ---
    def test_validation_xss_stripped(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "<b>Scrum Master</b>",
            "issuer": "<i>Scrum.org</i>",
            "date_range": "2025 - 2027",
            "description": "Valid description with <u>emphasis</u>",
            "icon": "📜",
            "image": "",
        }
        res = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Scrum Master")
        self.assertEqual(res.data["issuer"], "Scrum.org")
        self.assertEqual(res.data["description"], "Valid description with emphasis")

    def test_validation_empty_title_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "   ",
            "issuer": "Google",
            "date_range": "2025 - 2027",
            "description": "Desc",
            "icon": "📜",
            "image": "",
        }
        res = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", res.data)

    def test_validation_empty_issuer_rejected(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            "title": "Valid Certification",
            "issuer": "   ",
            "date_range": "2025 - 2027",
            "description": "Desc",
            "icon": "📜",
            "image": "",
        }
        res = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("issuer", res.data)

    # --- Search Query Tests ---
    def test_search_filters_certifications(self):
        Certification.objects.create(
            title="Google Associate Cloud Engineer",
            issuer="Google Cloud",
            date_range="2024 - 2027",
            description="Cloud engineering foundation",
            icon="☁️",
        )
        Certification.objects.create(
            title="Microsoft Certified: Azure Fundamentals",
            issuer="Microsoft",
            date_range="2024 - 2026",
            description="Azure fundamentals",
            icon="☁️",
        )

        # Search for 'Google'
        res = self.client.get(f"{self.list_url}?search=Google")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Google Associate Cloud Engineer")

        # Search for 'Azure'
        res_azure = self.client.get(f"{self.list_url}?search=Azure")
        self.assertEqual(res_azure.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_azure.data), 1)
        self.assertEqual(res_azure.data[0]["title"], "Microsoft Certified: Azure Fundamentals")

    # --- CSRF Protection Test ---
    def test_csrf_enforced_for_session_auth(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        login_success = csrf_client.login(username="owner_user", password="OwnerPassword123!")
        self.assertTrue(login_success)

        # POST without CSRF token should return 403 Forbidden
        payload = {
            "title": "CompTIA Security+",
            "issuer": "CompTIA",
            "date_range": "2025 - 2028",
            "description": "Cybersecurity",
            "icon": "🔒",
            "image": "",
        }
        res = csrf_client.post(self.list_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("CSRF", str(res.data.get("detail", "")))
