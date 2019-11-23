import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from articles.models import Article
from articles.models import ArticleBackup
from aylienapiclient import textapi
import asyncio



#scheduler process to update the databases after a specific interval
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_articles,'interval', seconds=120)
    scheduler.start()


#Method to store a single article in the backup database
async def storeArticle(id):
    print(id)
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

        if 'by' in x:
            article.by = x['by']
        else:
            article.by = " "

        if 'title' in x:
            article.title = x['title']
        else:
            article.title = " "

        if 'score' in x:
            article.score = x['score']
        else:
            article.score = " "

        sentiment = client.Sentiment({'text': article.title})
        article.sentimentPolarity = sentiment['polarity']
        article.save()

    except:
        print("Error in storing article")
        return



#Method to fetch all the data from Hacker News and store in the storage database and then to update the cache database.
async def main():
    print("Started updating databases")
    try:
        top_stories = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty").json()
        ArticleBackup.objects.all().delete()  #deleting contents of storage and adding new entries
        for i in range(0, 30, 3):  #using the asyncio module to run 3 processes at a time
            await asyncio.gather(storeArticle(str(top_stories[i])), storeArticle(str(top_stories[i + 1])),
                                 storeArticle(str(top_stories[i + 2])))

        #print(datetime.datetime.now())
        Article.objects.all().delete() #deleting contents of cache and adding entries from storage
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
        print("Database updation completed")
    except:
        print("Error in updating articles")
        return


def get_articles():
    #print(datetime.datetime.now())
    asyncio.run(main())
    #print(datetime.datetime.now())
