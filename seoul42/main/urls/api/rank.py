from django.urls import path

from main.api_views import RankApi
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('', RankApi)
# urlpatterns = router.urls
urlpatterns = [
	path('', RankApi.as_view({'get': 'list'}), name="rank_list_api"),
	path('<str:login>/', RankApi.as_view({'get': 'retrieve'}), name="rank_list_detail"),
]
