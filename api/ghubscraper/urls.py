from django.urls import include, path
from .views import RepoCreate, RepoList, CrawlSpider

urlpatterns = [
    path("create/", RepoCreate.as_view(), name="create-repo"),
    path("", RepoList.as_view()),
    path("crawl/", CrawlSpider.as_view()),
]
