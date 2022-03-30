from django.db import models
import re
from django.core.validators import RegexValidator

class Repo(models.Model):
    account = models.URLField(
        validators=[
            RegexValidator(
                "^https?://github.com/[a-z0-9](?:[a-z\d]|-(?=[a-z\d])){0,38}/?$",
                message="All URLs must be of the following format: "
                "http(s)://github.com/<account>(/)",
            )
        ]
    )

    repo = models.CharField(blank=True, max_length=255)
    about = models.CharField(blank=True, max_length=255)
    website_link = models.CharField(blank=True, max_length=255)

    stars = models.IntegerField(null=True, blank=True)
    forks = models.IntegerField(null=True, blank=True)
    watching = models.CharField(blank=True, max_length=255)

    main_branch_commit_count = models.IntegerField(null=True, blank=True)
    main_branch_latest_commit_author = models.CharField(blank=True, max_length=255)
    main_branch_latest_commit_datetime = models.DateTimeField(null=True, blank=True)
    main_branch_latest_commit_message = models.TextField(blank=True)

    release_count = models.IntegerField(null=True, blank=True)
    latest_release_tag = models.CharField(blank=True, max_length=255)
    latest_release_datetime = models.DateTimeField(null=True, blank=True)
    latest_release_changelog = models.TextField(blank=True)

    def __str__(self):
        return self.name
