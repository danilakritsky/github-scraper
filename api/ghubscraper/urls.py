from django.urls import include, path
from django.shortcuts import redirect
from .views import AddRepo, ListAccounts, CrawlPages, Index

urlpatterns = [
    path("", Index.as_view(), name='index'),
    path("add/", AddRepo.as_view(), name="add_repo"),
    path("accounts/", ListAccounts.as_view(), name="list_accounts"),
    path("crawl/", CrawlPages.as_view(), name="crawl_pages"),
]
