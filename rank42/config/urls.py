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
from django.urls import path, include
import main.views
import account.views

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

	# Manage App 관련 url
	path('manager/', include('manager.urls')),

	# piscine App 관련 url
	path('piscine/', include('piscine.urls')),
]
