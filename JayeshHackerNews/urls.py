from django.urls import path, include
from django.contrib import admin
from articles.views import *

admin.autodiscover()

urlpatterns = [
    path("", index, name="index"),  #path to home page
    path("admin/", admin.site.urls),
    path("api/listarticles/",ArtileList.as_view()) #API call to fetch the top articles as JSON
]
