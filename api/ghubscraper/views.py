from django.shortcuts import render
from .models import Repo
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RepoSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.parsers import JSONParser 

# use CreateAPIView for default form value
class RepoCreate(generics.CreateAPIView):
    serializer_class = RepoSerializer

    def post(self, request):
        # use many=False since only single object is expected
        serializer = RepoSerializer(data=request.data, many=False)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RepoCreate(generics.CreateView):
#     # API endpoint that allows creation of a new customer
#     queryset = Repo.objects.all()
#     serializer_class = RepoSerializer    


class RepoList(generics.ListAPIView):
    # API endpoint that allows customer to be viewed.
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer