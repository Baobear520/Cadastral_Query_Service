from django.urls import include, path
from query_api import views


urlpatterns = [
    path('query/', views.QueryViewSet.as_view({'post':'create'})),
    path('result/', views.ResultViewSet.as_view({'post':'create'})),
    #path('ping/', views),
    path('history/', views.HistoryViewSet.as_view({'get':'list'}))
]