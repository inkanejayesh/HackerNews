from django.db import models

# Create your models here.

#The model class which is used to send data to the home page. Consider this as a cache.
class Article(models.Model):
    by = models.CharField("Username",max_length=100,null=True)
    title = models.CharField(max_length=100)
    url = models.TextField(blank=True)
    score = models.IntegerField()
    sentimentPolarity = models.CharField(max_length=100)

    def __str__(self):
        return self.title

#This model class is used to store the data that we fetch from Hacker News API call. Consider this as storage.
class ArticleBackup(models.Model):
    by = models.CharField("Username",max_length=100,null=True)
    title = models.CharField(max_length=100)
    url = models.TextField(blank=True)
    score = models.IntegerField()
    sentimentPolarity = models.CharField(max_length=100)

    def __str__(self):
        return self.title
