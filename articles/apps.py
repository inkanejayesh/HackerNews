from django.apps import AppConfig


class HelloConfig(AppConfig):
    name = 'articles'

    def ready(self):
        from articles.articles_scheduler import update_articles
        update_articles.start()