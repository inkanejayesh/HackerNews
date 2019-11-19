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

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    x = requests.get("http://localhost:5000/listarticles").json()
    return render(request, "articles.html", context={"articles": Article.objects.all()})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def articlelist(request):
    top_stories = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty").json()
    client = textapi.Client("9cf3ddcd", "b3b1304158f0a52adc0f1f970059edc3")
    for i in range(2):
        x = requests.get(
            "https://hacker-news.firebaseio.com/v0/item/" + str(top_stories[i]) + ".json?print=pretty").json()
        article = Article()
        article.url = x['url']
        article.title = x['title']
        article.score = x['score']
        article.username = x['by']
        sentiment = client.Sentiment({'text': x['title']})
        article.sentimentPolarity = sentiment['polarity']
        article.save()

class ArtileList(APIView):
    def get(self,request):
        articlelist(request)
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        print("Hello")
        return Response(serializer.data)

    def post(self):
        pass
