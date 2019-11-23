#Management class to update the databases manually


import requests
import datetime
from aylienapiclient import textapi
from django.core.management.base import BaseCommand
from articles.models import Article, ArticleBackup
import asyncio

async def storeArticle(id):
    # print(id)
    await asyncio.sleep(2)
    try:
        client = textapi.Client("9cf3ddcd", "b3b1304158f0a52adc0f1f970059edc3")
        x = requests.get(
            "https://hacker-news.firebaseio.com/v0/item/" + str(id) + ".json?print=pretty").json()
        article = ArticleBackup()
        if 'url' in x:
            article.url = x['url']
        else:
            article.url = "  "
        article.title = x['title']
        article.score = x['score']
        article.by = x['by']
        sentiment = client.Sentiment({'text': x['title']})
        article.sentimentPolarity = sentiment['polarity']
        article.save()

    except:
        print("Error in storing article")
        return

async def main():
    try:
        top_stories = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty").json()
        ArticleBackup.objects.all().delete()
        for i in range(0, 30, 3):
            await asyncio.gather(storeArticle(str(top_stories[i])), storeArticle(str(top_stories[i + 1])),
                                 storeArticle(str(top_stories[i + 2])))

        #print(datetime.datetime.now())
        Article.objects.all().delete()
        for item in ArticleBackup.objects.all():
            article = Article()
            article.url = item.url
            article.title = item.title
            article.score = item.score
            article.by = item.by
            article.sentimentPolarity = item.sentimentPolarity
            # print(type(article))
            article.save()
        #print(datetime.datetime.now())
    except:
        print("Error in updating articles")
        return

class Command(BaseCommand):

    def handle(self, *args, **options):
        asyncio.run(main())