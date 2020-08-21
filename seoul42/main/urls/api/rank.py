from django.urls import path

from main.api_views import RankListApi, RankDetailApi


urlpatterns = [
	path('', RankListApi.as_view(), name="rank_list_api"),
	path('<str:login>/', RankDetailApi.as_view(), name="rank_list_detail"),
]
