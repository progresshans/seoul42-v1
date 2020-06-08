from django.urls import path
from . import views

urlpatterns = [
	path('manage/', views.PiscineManagePage.as_view(), name="manage"),
	path('manage/update/piscine-ft-user', views.UpdatePiscineFtUser.as_view(), name="update_piscine_ft_user"),
	path('manage/make/piscine-ft-user/', views.MakePiscineFtUser.as_view(), name="make_piscine_ft_user"),
]