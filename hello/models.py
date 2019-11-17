from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Article(models.Model):
    by = models.CharField("Username",max_length=100,null=True)
    title = models.CharField(max_length=100)
    url = models.TextField(blank=True)
    score = models.IntegerField()
    sentimentPolarity = models.CharField(max_length=100)

    def __str__(self):
        return self.title
