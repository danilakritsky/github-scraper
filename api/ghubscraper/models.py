from django.db import models

# Create your models here.

class Repo(models.Model):
    account=models.URLField()
    repo=models.CharField(null=True)
    about=models.CharField(null=True)
    website_link=models.CharField(null=True)
    stars=models.IntegerField(null=True)
    forks=models.IntegerField(null=True)
    watching=models.CharField(null=True)
    main_branch_commit_count=models.IntegerField(null=True)
    main_branch_latest_commit_author=models.CharField(null=True)
    main_branch_latest_commit_datetime=models.DateTimeField(null=True)
    main_branch_latest_commit_message=models.TextField(null=True)
    release_count=models.IntegerField(null=True)
    latest_release_tag=models.CharField(null=True)
    latest_release_datetime=models.DateTimeField(null=True)
    latest_release_changelog=models.TextField(null=True)

    def __str__(self):
        return self.name