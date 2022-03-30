from django.shortcuts import render
from .models import Repo
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RepoSerializer, CrawlSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Repo
import requests
import datetime
import os

# use CreateAPIView for default form value
class RepoCreate(generics.CreateAPIView):
    serializer_class = RepoSerializer

    def get(self, request):
        return Response(
            {
                "info": "Make a POST request against this endpoint (/create/) to add new repo data."
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        # use many=False since only single object is expected
        serializer = RepoSerializer(data=request.data, many=False)
        data = request.data
        data["account"] = clean_url(data["account"])
        if serializer.is_valid():

            # drop existing items
            queryset = Repo.objects.filter(account=data["account"], repo=data["repo"])
            if queryset:
                for record in queryset:
                    record.delete()

            # save new item
            instance = Repo(**data)
            instance.account = clean_url(data["account"])
            instance.save()

            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrawlSpider(generics.CreateAPIView):
    serializer_class = CrawlSerializer

    def get(self, request):
        return Response(
            {
                "info": "Make a POST request against this endpoint (/crawl/) to start crawling."
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        # use many=False since only single object is expected
        serializer = CrawlSerializer(data=request.data, many=False)
        if not request.data["start_urls"]:
            return Response("No URLs have been provided.", status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            validated_urls = []
            for url in request.data["start_urls"]:
                validated_urls.append(clean_url(url))

            # remove duplicates
            request.data["start_urls"] = list(set(validated_urls))

            response = requests.post(
                (os.getenv("SCRAPYD_HOST") or "http://scrapyd:6800") + "/schedule.json",
                data={
                    "start_urls": ",".join(request.data["start_urls"]),
                    "project": "scraper",
                    "spider": "scraper_api",
                    "jobid": datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S"),
                },
            )
            if response.status_code == 200:
                return Response(request.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "Error connecting to scrapyd server.", status.HTTP_400_BAD_REQUEST
                )

        return Response(
            "All URLs must be of the following format: "
            "http(s)://github.com/<account>(/)",
            status=status.HTTP_400_BAD_REQUEST,
        )


class RepoList(generics.ListAPIView):
    # API endpoint that allows customer to be viewed.
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer


def clean_url(url: str) -> str:
    url = url.replace("http:", "https:")
    return url[:-1] if url[-1] == "/" else url
