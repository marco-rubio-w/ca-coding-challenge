from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

Reviewer = get_user_model()


class Company(models.Model):
    """Stores a company to be reviewed"""

    MAX_NAME_LENGTH: int = 64

    name: str = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name=_("Company name")
    )


class CompanyReview(models.Model):
    """Stores a company review posted by a user"""

    MAX_TITLE_LENGTH: int = 64
    MAX_SUMMARY_LENGTH: int = 10 ** 4

    reviewer = models.ForeignKey(
        Reviewer,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("Reviewer"),
    )
    company: Company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name=_("Company to review")
    )
    rating: int = models.IntegerField(verbose_name=_("Rating"))
    title = models.CharField(
        max_length=MAX_TITLE_LENGTH, verbose_name=_("Title")
    )
    summary = models.TextField(verbose_name=_("Summary"))
    ip_address = models.GenericIPAddressField(
        verbose_name=_("Submitter address")
    )
    date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Submission date")
    )
