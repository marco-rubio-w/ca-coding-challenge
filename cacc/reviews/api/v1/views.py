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
