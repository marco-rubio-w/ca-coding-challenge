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

    def validate_rating(self, value):
        """Validates the range for the rating"""

        min_value = models.CompanyReview.MIN_RATING_VALUE
        max_value = models.CompanyReview.MIN_RATING_VALUE

        if min_value > value or max_value < value:
            raise serializers.ValidationError("Rating must be within and ")

        return value

    def create(self, validated_data):
        """Creates a CompanyReview object"""
        request = self.context["request"]
        meta = request.META

        # Add the reviewer data
        validated_data["reviewer"] = request.user

        # Add the ip address data
        if "HTTP_X_FORWARDED_FOR" in meta:
            header_data = meta.get("HTTP_X_FORWARDED_FOR")
            addresses = header_data.replace(" ", "").split(",")
            validated_data["ip_address"] = addresses[0]

        else:
            validated_data["ip_address"] = meta.get("REMOTE_ADDR")

        return super().create(validated_data)

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
