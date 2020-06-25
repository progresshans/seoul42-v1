from django.urls import path
from . import views

urlpatterns = [
	path('', views.ClubList.as_view(), name="club_list"),
	path('add/', views.ClubAdd.as_view(), name="club_add"),
]