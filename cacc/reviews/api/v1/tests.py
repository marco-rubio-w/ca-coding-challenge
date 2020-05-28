import random

from django.urls import reverse
from rest_framework.test import APITestCase

from ... import models

V1_REVIEW_LIST = "api-v1-review-list"
V1_REVIEW_DETAIL = "api-v1-review-detail"
V1_REVIEW_LIST_URL = reverse(V1_REVIEW_LIST)

ADMIN_USER_USERNAME = "admin"
REGULAR_USER_USERNAME = "regular"


class TestCompanyReviewListingEndpoint(APITestCase):
    """Tests for the company review listing endpoint"""

    fixtures = ["test/companies", "test/users", "test/reviews"]

    def test_unauthenticated_access_is_rejected(self):
        """Tests that unauthenticated access is rejected"""

        url = V1_REVIEW_LIST_URL

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_access_is_allowed(self):
        """Tests that authenticated user access is allowed"""

        url = V1_REVIEW_LIST_URL
        usernames = [REGULAR_USER_USERNAME, ADMIN_USER_USERNAME]

        for username in usernames:
            reviewer = models.Reviewer.objects.filter(
                username=username
            ).first()

            self.client.force_authenticate(user=reviewer)

            response = self.client.get(url, format="json")
            self.assertEqual(response.status_code, 200)

    def test_regular_users_can_retrieve_only_own_reviews(self):
        """Tests that regular users can retrieve only own reviews"""

        url = V1_REVIEW_LIST_URL
        users = models.Reviewer.objects.filter(is_staff=False)
        expected_records = {}

        models.CompanyReview.objects.all().delete()

        for user in users:
            # Create between 4 and 20 reviews per user
            expected_records[user] = random.randint(4, 20)
            for index in range(0, expected_records[user]):
                models.CompanyReview.objects.create(
                    title=f"Title {index}",
                    summary=f"Summary {index}",
                    company=models.Company.objects.first(),
                    rating=1,
                    reviewer=user,
                    ip_address="12:34:56:78",
                )

        for user in users:
            record_count = models.CompanyReview.objects.filter(
                reviewer=user
            ).count()
            self.assertEqual(record_count, expected_records[user])

            self.client.force_authenticate(user=user)
            response = self.client.get(url, format="json")
            self.assertEqual(response.status_code, 200)
            content = response.json()
            self.assertIsInstance(content, list)
            self.assertEqual(record_count, len(content))

            for record in content:
                self.assertEqual(record["reviewer"], user.id)

    def test_admin_users_can_retrieve_all_reviews(self):
        """Tests that admin users can retrieve all reviews"""

        url = V1_REVIEW_LIST_URL
        users = models.Reviewer.objects.filter(is_staff=False)
        expected_records = 0

        models.CompanyReview.objects.all().delete()

        for user in users:
            # Create between 4 and 20 reviews per user
            for index in range(0, random.randint(4, 20)):
                models.CompanyReview.objects.create(
                    title=f"Title {index}",
                    summary=f"Summary {index}",
                    company=models.Company.objects.first(),
                    rating=1,
                    reviewer=user,
                    ip_address="12:34:56:78",
                )
                expected_records += 1

        user = models.Reviewer.objects.filter(is_staff=True).first()

        record_count = models.CompanyReview.objects.count()
        self.assertEqual(record_count, expected_records)

        self.client.force_authenticate(user=user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        content = response.json()
        self.assertIsInstance(content, list)
        self.assertEqual(record_count, len(content))


class TestCompanyReviewCreationEndpoint(APITestCase):
    """Tests for the company review creation endpoint"""

    fixtures = ["test/companies", "test/users", "test/reviews"]

    def test_unauthenticated_access_is_rejected(self):
        """Tests that unauthenticated access is rejected"""

        url = V1_REVIEW_LIST_URL

        data = {
            "title": "Title",
            "summary": "Summary",
            "company": models.Company.objects.first().id,
            "rating": 1,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 401)



class TestCompanyReviewRetrievalEndpoint(APITestCase):
    """Tests for the company review retrieval endpoint"""

    fixtures = ["test/companies", "test/users", "test/reviews"]

    def test_unauthenticated_access_is_rejected(self):
        """Tests that unauthenticated access is rejected"""

        review = models.CompanyReview.objects.first()
        url = reverse(V1_REVIEW_DETAIL, kwargs={"pk": review.id})

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 401)


class TestCompanyReviewUpdateEndpoint(APITestCase):
    """Tests for the company review update endpoint"""

    fixtures = ["test/companies", "test/users", "test/reviews"]

    def test_unauthenticated_access_is_rejected(self):
        """Tests that unauthenticated access is rejected"""

        review = models.CompanyReview.objects.first()
        url = reverse(V1_REVIEW_DETAIL, kwargs={"pk": review.id})
        data = {"title": "New title"}

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 401)


class TestCompanyReviewDeletionEndpoint(APITestCase):
    """Tests for the company review deletion endpoint"""

    fixtures = ["test/companies", "test/users", "test/reviews"]

    def test_unauthenticated_access_is_rejected(self):
        """Tests that unauthenticated access is rejected"""

        review = models.CompanyReview.objects.first()
        url = reverse(V1_REVIEW_DETAIL, kwargs={"pk": review.id})

        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, 401)
