from django.urls import include, path
from .views import RepoCreate, RepoList

urlpatterns = [
    path('create/', RepoCreate.as_view(), name='create-repo'),
    path('', RepoList.as_view()),
]

