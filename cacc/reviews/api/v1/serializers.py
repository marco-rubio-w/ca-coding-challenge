from rest_framework import serializers
from ... import models


class ReviewerSerializer(serializers.ModelSerializer):
    """Serializes and deserializes Reviewer model data"""

    class Meta(object):
        """Configuration for this serializer"""

        model = models.Reviewer
        fields = ("id", "first_name", "last_name")


class CompanySerializer(serializers.ModelSerializer):
    """Serializes and deserializes Company model data"""

    class Meta(object):
        """Configuration for this serializer"""

        model = models.Company
        fields = ("id", "name")


class CompanyReviewSerializer(serializers.ModelSerializer):
    """Serializes and deserializes CompanyReview model data"""

    reviewer = serializers.ModelField(
        models.CompanyReview()._meta.get_field("reviewer"),
        required=False,
        read_only=True,
    )
    ip_address = serializers.ReadOnlyField()

    class Meta:
        """Configuration for this serializer"""

        model = models.CompanyReview
        fields = (
            "company",
            "rating",
            "title",
            "summary",
            "ip_address",
            "date",
            "reviewer",
        )
