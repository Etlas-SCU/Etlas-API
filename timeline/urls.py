from django.urls import path

from .views import HistoryTimelineList, HistoryTimelineDetail

app_name = 'timeline'
urlpatterns = [
    path('', HistoryTimelineList.as_view(), name='historytimeline-list'),
    path('<int:pk>/', HistoryTimelineDetail.as_view(), name='historytimeline-detail'),
]
