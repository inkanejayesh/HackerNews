from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ArticleSerializer
from .models import Article
from aylienapiclient import textapi
from articles.management.commands.get_articles import Command
import multiprocessing

#Method to render the home page
def index(request):
    return render(request, "articles.html", context={"articles": Article.objects.all()})

#APIView class to send the data as JSON
class ArtileList(APIView):
    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        print("Hello")
        return Response(serializer.data)

    def post(self):
        pass