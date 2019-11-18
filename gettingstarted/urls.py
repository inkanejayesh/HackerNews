from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

from hello.views import *

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", index, name="index"),
    path("db/", db, name="db"),
    path("admin/", admin.site.urls),
    path("articles/",index),
    path("listarticles/",ArtileList.as_view())
]
