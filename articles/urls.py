from django.urls import path
from . import views

urlpatterns = [
    path("",views.ArticlesList.as_view()),
    path("<int:pk>/",views.GetSingleArticle.as_view())
]