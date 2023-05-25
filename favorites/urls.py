from django.urls import path

from . import views

app_name = "favorites"
urlpatterns = [
    path("", views.FavoriteListView.as_view(), name="list"),
    path("monument/add/", views.FavoriteMonumentCreateView.as_view(), name="monument-add"),
    path("article/add/", views.FavoriteArticleCreateView.as_view(), name="article-add"),
    path("monument/delete/", views.FavoriteMonumentDeleteView.as_view(), name="monument-delete"),
    path("article/delete/", views.FavoriteArticleDeleteView.as_view(), name="article-delete"),
]
