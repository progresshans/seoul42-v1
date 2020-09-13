from django.urls import path

from ..views import WriteReport


urlpatterns = [
	path('', WriteReport.as_view(), name="write_report"),
]
