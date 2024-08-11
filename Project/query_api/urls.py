from django.urls import include, path
from query_api import views


urlpatterns = [
    path('query/', views.QueryViewSet.as_view({'post':'create'})),
    #path('result/', views),
    #path('ping/', views),
    #path('history/', views),

]