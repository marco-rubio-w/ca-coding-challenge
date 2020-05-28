from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(
    "companies", views.CompanyViewSet, basename="api-v1-company",
)
router.register(
    "reviews", views.CompanyReviewViewSet, basename="api-v1-review",
)
router.register(
    "reviewers", views.ReviewerViewSet, basename="api-v1-reviewer",
)

urlpatterns = router.urls
