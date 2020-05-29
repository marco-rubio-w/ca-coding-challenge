from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

urlpatterns = [
    path("", views.ReviewListView.as_view(), name="review-list"),
    path(
        "reviewer/<int:reviewer>",
        views.UserReviewListView.as_view(),
        name="review-list-by-user",
    ),
    path(
        "review/<int:review>",
        views.ReviewDetaiView.as_view(),
        name="review-detail",
    ),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/", include("reviews.api.urls")),
    path(
        "login",
        auth_views.LoginView.as_view(template_name="reviews/login.html"),
        name="login",
    ),
    path(
        "logout",
        auth_views.LogoutView.as_view(next_page="review-list"),
        name="logout",
    ),
]
