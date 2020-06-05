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
from django.urls import path
import main.views

urlpatterns = [
	# Admin 관련 url
	path('admin/', admin.site.urls),

	# Main 페이지 관련 url
	path('', main.views.Main.as_view(), name="main"),
	path('list/', main.views.List.as_view(), name="list"),
	path('search/<str:login>/', main.views.Search.as_view(), name="search"),

	# Manage 페이지 관련 url
	path('manage/', main.views.ManagePage.as_view(), name="manage"),
	path('manage/make/coalition', main.views.MakeCoalition.as_view(), name="make_coalition"),
	path('manage/make/ft-user', main.views.MakeFtUser.as_view(), name="make_ft_user"),
	path('manage/migrate/move-coalition-point', main.views.MoveCoalitionPoint.as_view(), name="move_coalition_point"),
]
