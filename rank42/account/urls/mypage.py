from django.urls import path
from .. import views

urlpatterns = [
	path('', views.MyPage.as_view(), name="mypage"),
]