from rest_framework import serializers 
from ghubscraper.models import Repo
 
 
class RepoSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Repo
        fields = (
            'account',
            'repo',
            'about',
            'website_link',
            'stars',
            'forks',
            'watching',
            'main_branch_commit_count',
            'main_branch_latest_commit_author',
            'main_branch_latest_commit_datetime',
            'main_branch_latest_commit_message',
            'release_count',
            'latest_release_tag',
            'latest_release_datetime',
            'latest_release_changelog',         
        )