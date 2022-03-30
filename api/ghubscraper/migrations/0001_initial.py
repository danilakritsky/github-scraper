# Generated by Django 4.0.3 on 2022-03-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Repo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account", models.URLField()),
                ("repo", models.CharField(blank=True, max_length=255)),
                ("about", models.CharField(blank=True, max_length=255)),
                ("website_link", models.CharField(blank=True, max_length=255)),
                ("stars", models.IntegerField(blank=True, null=True)),
                ("forks", models.IntegerField(blank=True, null=True)),
                ("watching", models.CharField(blank=True, max_length=255)),
                (
                    "main_branch_commit_count",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "main_branch_latest_commit_author",
                    models.CharField(blank=True, max_length=255),
                ),
                (
                    "main_branch_latest_commit_datetime",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("main_branch_latest_commit_message", models.TextField(blank=True)),
                ("release_count", models.IntegerField(blank=True, null=True)),
                ("latest_release_tag", models.CharField(blank=True, max_length=255)),
                (
                    "latest_release_datetime",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("latest_release_changelog", models.TextField(blank=True)),
            ],
        ),
    ]
