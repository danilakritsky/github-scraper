"""This module contains serializers for data."""

from rest_framework import serializers

from ghubscraper.models import Repo


class RepoSerializer(serializers.ModelSerializer):
    """Serializer for repo data."""

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
    "Serializer for a list of URLs to scrape."

    start_urls = serializers.ListField(
        child=serializers.RegexField(
            r"^https?://github.com/[a-z0-9](?:[a-z\d]|-(?=[a-z\d])){0,38}/?$"
        )
    )


class AccountSerializer(serializers.Serializer):
    """Serializer for account URL."""

    account = serializers.RegexField(
        r"^https?://github.com/[a-z0-9](?:[a-z\d]|-(?=[a-z\d])){0,38}/?$"
    )
