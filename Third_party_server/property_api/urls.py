from django.urls import path
from property_api.views import PropertyView

urlpatterns = [
    path('result/', PropertyView.as_view(),name='result')
]