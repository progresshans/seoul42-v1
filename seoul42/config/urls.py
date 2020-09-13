"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import main.views
import account.views

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
	openapi.Info(
		title="Seoul42 API",
		default_version="v1",
		description="Seoul42의 API 문서입니다.",
		contact=openapi.Contact(email="progresshans@gmail.com"),
		license=openapi.License(name="progresshans"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
	# Admin 관련 url
	path('admin/', admin.site.urls),

	# Account 관련 url
	path('login/', account.views.SignInPage.as_view(), name="login"),
	path('logout/', account.views.LogOut.as_view(), name="logout"),
	path('ft-login/', account.views.FtApiSignIn.as_view(), name="ft_login"),

	# Account-Mypage 관련 url
	path('mypage/', include('account.urls.mypage')),

	# Club 관련 url
	path('club/', include('club.urls')),

	# Main App 관련 url
	path('', main.views.Main.as_view(), name="main"),
	path('list/', main.views.List.as_view(), name="list"),
	path('search/<str:login>/', main.views.Search.as_view(), name="search"),
	path('update/ft-user/', main.views.UpdateFtUser.as_view(), name="update_ft_user"),
	path('github/', main.views.GithubRank.as_view(), name="github_rank"),

	# Main-Api-Rank 관련 url
	path('api/rank/', include('main.urls.api.rank')),

	# Manage App 관련 url
	path('manager/', include('manager.urls')),

	# piscine App 관련 url
	path('piscine/', include('piscine.urls')),

	# Toy-Report 관련 url
	path('toy/report', include('toy.urls.report')),

	# API 문서 관련 url
	re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='api_swagger_json'),
	re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='api_swagger'),
	re_path(r'^api/docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='api_docs'),
]
