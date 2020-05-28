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

    def test_authenticated_user_object_creation(self):
        """Tests that authenticated user object creation"""

        url = V1_REVIEW_LIST_URL
        reviewers = models.Reviewer.objects.all()

        for reviewer in reviewers:
            data = {
                "title": "Title",
                "summary": "Summary",
                "company": models.Company.objects.first().id,
                "rating": 1,
            }

            self.client.force_authenticate(user=reviewer)

            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, 201)

            created_object = response.json()
            self.assertEqual(created_object["reviewer"], reviewer.id)

    def test_rating_field_only_accepts_integers_within_range(self):
        """Tests that the rating field only accepts integers within range"""

        url = V1_REVIEW_LIST_URL
        min_value = models.CompanyReview.MIN_RATING_VALUE
        max_value = models.CompanyReview.MIN_RATING_VALUE
        range_start = min_value - 5
        range_end = min_value + 5

        base_data = {
            "title": "Title",
            "summary": "Summary",
            "company": models.Company.objects.first().id,
        }

        reviewer = models.Reviewer.objects.filter(is_staff=False).first()

        self.client.force_authenticate(user=reviewer)

        for value in range(range_start, range_end):
            data = {"rating": value, **base_data}
            response = self.client.post(url, data, format="json")
            content = response.json()

            if min_value <= value <= max_value:
                self.assertEqual(response.status_code, 201)
                self.assertEqual(content["rating"], value)

            else:
                self.assertEqual(response.status_code, 400)
                self.assertIn("rating", content)

    def test_ip_client_address_is_added_to_created_object(self):
        """Tests that client ip address is added to created object"""

        url = V1_REVIEW_LIST_URL
        remote_address = "82.73.64.55"
        data = {
            "title": "Title",
            "summary": "Summary",
            "company": models.Company.objects.first().id,
            "rating": 1,
        }

        self.client.force_authenticate(
            user=models.Reviewer.objects.filter(is_staff=False).first()
        )

        # Test regular address
        response = self.client.post(
            url, data, format="json", REMOTE_ADDR=remote_address
        )
        content = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("ip_address", content)
        self.assertEqual(content["ip_address"], remote_address)

        # Test forwarded address
        forwarded_header = f"{remote_address}, 103.0.123.105, 40.42.3.28"
        response = self.client.post(
            url, data, format="json", HTTP_X_FORWARDED_FOR=forwarded_header
        )
        content = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("ip_address", content)
        self.assertEqual(content["ip_address"], remote_address)


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
