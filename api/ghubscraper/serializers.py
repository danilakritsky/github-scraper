import re

from django.core.exceptions import ValidationError

from rest_framework import serializers
from ghubscraper.models import Repo


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = (
            "account",
            "repo",
            "about",
            "website_link",
            "stars",
            "forks",
            "watching",
            "main_branch_commit_count",
            "main_branch_latest_commit_author",
            "main_branch_latest_commit_datetime",
            "main_branch_latest_commit_message",
            "release_count",
            "latest_release_tag",
            "latest_release_datetime",
            "latest_release_changelog",
        )


class CrawlSerializer(serializers.Serializer):

    start_urls = serializers.ListField(
        child=serializers.RegexField(
            "^https?://github.com/[a-z0-9](?:[a-z\d]|-(?=[a-z\d])){0,38}/?$"
        )
    )
