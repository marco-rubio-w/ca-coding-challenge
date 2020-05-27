from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    """Stores a company to be reviewed"""

    MAX_NAME_LENGTH: int = 64

    name: str = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name=_("Company name")
    )
