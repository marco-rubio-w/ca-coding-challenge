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
