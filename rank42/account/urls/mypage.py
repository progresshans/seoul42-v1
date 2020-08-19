from django.urls import path
from .. import views

urlpatterns = [
	path('', views.MyPage.as_view(), name="mypage"),
	path('add/github/id/', views.AddGithubId.as_view(), name="add_github_id"),
]