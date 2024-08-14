from rest_framework.routers import DefaultRouter
from query_api import views


router = DefaultRouter()

router.register(r'ping', views.PingViewSet,basename='ping')
router.register(r'query', views.QueryViewSet,basename='query')
router.register(r'result', views.ResultViewSet,basename='result')
router.register(r'history', views.HistoryViewSet,basename='history')

urlpatterns = router.urls
