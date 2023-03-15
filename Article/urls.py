from django.urls import path
from . import views

urlpatterns = [
    path("articles/",views.ArticlesList.as_view()),
    path("articles/<int:pk>",views.GetSingleArticle.as_view()),   
]