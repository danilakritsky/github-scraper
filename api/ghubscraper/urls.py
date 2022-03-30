"""This module contains endpoints and their views."""

from django.urls import path

from .views import AddRepo, CrawlPages, Index, ListAccounts, Stats

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("add/", AddRepo.as_view(), name="add_repo"),
    path("accounts/", ListAccounts.as_view(), name="list_accounts"),
    path("crawl/", CrawlPages.as_view(), name="crawl_pages"),
    path("stats/", Stats.as_view(), name="stats"),
]
