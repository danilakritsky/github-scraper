# Generated by Django 4.0.3 on 2022-03-30 23:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.URLField(validators=[django.core.validators.RegexValidator('^https?://github.com/[a-z0-9](?:[a-z\\d]|-(?=[a-z\\d])){0,38}/?$', message='All URLs must be of the following format: http(s)://github.com/<account>(/)')])),
                ('repo', models.CharField(blank=True, max_length=255)),
                ('about', models.CharField(blank=True, max_length=255)),
                ('website_link', models.CharField(blank=True, max_length=255)),
                ('stars', models.IntegerField(blank=True, null=True)),
                ('forks', models.IntegerField(blank=True, null=True)),
                ('watching', models.CharField(blank=True, max_length=255)),
                ('main_branch_commit_count', models.IntegerField(blank=True, null=True)),
                ('main_branch_latest_commit_author', models.CharField(blank=True, max_length=255)),
                ('main_branch_latest_commit_datetime', models.DateTimeField(blank=True, null=True)),
                ('main_branch_latest_commit_message', models.TextField(blank=True)),
                ('release_count', models.IntegerField(blank=True, null=True)),
                ('latest_release_tag', models.CharField(blank=True, max_length=255)),
                ('latest_release_datetime', models.DateTimeField(blank=True, null=True)),
                ('latest_release_changelog', models.TextField(blank=True)),
            ],
        ),
    ]
