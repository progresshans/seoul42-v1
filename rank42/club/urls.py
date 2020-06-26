from django.urls import path
from . import views

urlpatterns = [
	path('', views.ClubList.as_view(), name="club_list"),
	path('add/', views.ClubAdd.as_view(), name="club_add"),
	path('<int:club_id>/', views.ClubDetail.as_view(), name="club_detail"),
	path('<int:club_id>/join/', views.ClubJoin.as_view(), name="club_detail"),
]