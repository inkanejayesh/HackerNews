import requests
from aylienapiclient import textapi
from django.core.management.base import BaseCommand

from hello.models import Article


class Command(BaseCommand):

    def handle(self, *args, **options):
        top_stories = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty").json()
        client = textapi.Client("9cf3ddcd", "b3b1304158f0a52adc0f1f970059edc3")
        for count,i in enumerate(top_stories):
            x = requests.get(
                "https://hacker-news.firebaseio.com/v0/item/" + str(i) + ".json?print=pretty").json()
            article = Article()
            article.url = x['url']
            article.title = x['title']
            article.score = x['score']
            article.by = x['by']
            sentiment = client.Sentiment({'text': x['title']})
            article.sentimentPolarity = sentiment['polarity']
            article.save()
            #print("Saved in db")
            print(count)