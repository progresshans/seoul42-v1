from django.urls import path
from . import views

urlpatterns = [
	path('', views.ClubList.as_view(), name="club_list"),
]