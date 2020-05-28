from rest_framework import permissions, viewsets

from ... import models
from . import serializers


class ReviewerViewSet(viewsets.ReadOnlyModelViewSet):
    """Responds to requests for Company objects"""

    queryset = models.Reviewer.objects.all()
    serializer_class = serializers.ReviewerSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """Responds to requests for Company objects"""

    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer


class CompanyReviewViewSet(viewsets.ModelViewSet):
    """Responds to requests for CompanyReview objects"""

    queryset = models.CompanyReview.objects.all()
    serializer_class = serializers.CompanyReviewSerializer

    def get_permissions(self):
        """Gets the permissions for this class"""
        permission_classes = []

        if self.action in ["list", "create", "retrieve"]:
            permission_classes = [permissions.IsAuthenticated]

        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission_class() for permission_class in permission_classes]

    def get_queryset(self):
        """Filters the query based on the current user"""

        user = self.request.user
        queryset = super().get_queryset()

        # Make sure regular users can access their own reviews only
        if not user.is_staff:
            queryset = queryset.filter(reviewer=user)

        return queryset
