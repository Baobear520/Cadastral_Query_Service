from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'query', views.QueryViewSet,basename='query')
router.register(r'result', views.ResultViewSet,basename='result')
router.register(r'history', views.HistoryViewSet,basename='history')

urlpatterns = router.urls
