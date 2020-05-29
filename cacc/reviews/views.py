from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

from . import models


class AdminOnlyViewMixin(UserPassesTestMixin):
    """Mixin for enforcing administrator only access"""

    def test_func(self):
        """Tests whether the user is an admin or not"""
        return self.request.user.is_staff


class ReviewListView(AdminOnlyViewMixin, TemplateView):
    """Lists all company reviews"""

    template_name = "reviews/review-list.html"

    def get_context_data(self, **kwargs):
        """Gets context data for this view"""

        context = super().get_context_data(**kwargs)

        context["reviews"] = models.CompanyReview.objects.all()

        return context


class UserReviewListView(AdminOnlyViewMixin, TemplateView):
    """Lists all reviews by a user"""

    template_name = "reviews/review-list.html"

    def get_context_data(self, *args, **kwargs):
        """Gets context data for this view"""
        context = super().get_context_data(**kwargs)

        reviewer_id = kwargs.get("reviewer")
        reviewer = models.Reviewer.objects.get(id=reviewer_id)
        reviews = models.CompanyReview.objects.filter(reviewer=reviewer)

        context["focused_reviewer"] = reviewer
        context["reviews"] = reviews

        return context


class ReviewDetaiView(AdminOnlyViewMixin, TemplateView):
    """Shows the detail for a review"""

    template_name = "reviews/review-detail.html"

    def get_context_data(self, *args, **kwargs):
        """Gets context data for this view"""
        context = super().get_context_data(**kwargs)

        review_id = kwargs.get("review")
        review = models.CompanyReview.objects.get(id=review_id)

        context["review"] = review
        context["max_rating"] = models.CompanyReview.MAX_RATING_VALUE

        return context
