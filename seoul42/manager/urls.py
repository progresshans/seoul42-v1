from django.urls import path
from . import views

urlpatterns = [
	path('', views.ManagePage.as_view(), name="manage"),
	path('make/coalition/', views.MakeCoalition.as_view(), name="make_coalition"),
	path('make/ft-user/', views.MakeFtUser.as_view(), name="make_ft_user"),
	path('migrate/move-coalition-point/', views.MoveCoalitionPoint.as_view(), name="move_coalition_point"),
]
