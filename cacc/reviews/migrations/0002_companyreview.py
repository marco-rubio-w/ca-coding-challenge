from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyReview",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rating", models.IntegerField(verbose_name="Rating")),
                (
                    "title",
                    models.CharField(max_length=64, verbose_name="Title"),
                ),
                ("summary", models.TextField(verbose_name="Summary")),
                (
                    "ip_address",
                    models.GenericIPAddressField(
                        verbose_name="Submitter address"
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Submission date"
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reviews.Company",
                        verbose_name="Company to review",
                    ),
                ),
                (
                    "reviewer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Reviewer",
                    ),
                ),
            ],
        ),
    ]
