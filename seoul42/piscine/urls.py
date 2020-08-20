from django.urls import path
from . import views

urlpatterns = [
	path('', views.Index.as_view(), name="piscine_index"),
	path('list/', views.List.as_view(), name="piscine_list"),
	path('manage/', views.PiscineManagePage.as_view(), name="piscine_manage"),
	path('manage/update/piscine-ft-user', views.UpdatePiscineFtUser.as_view(), name="update_piscine_ft_user"),
	path('manage/make/piscine-ft-user/', views.MakePiscineFtUser.as_view(), name="make_piscine_ft_user"),
	path('manage/delete/piscine-ft-user/', views.DeletePiscineFtUser.as_view(), name="delete_piscine_ft_user"),
]