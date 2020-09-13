import requests

from django.shortcuts import render
from django.views import View

from .utils import get_weekday_list


class WriteReport(View):
	def get(self, request):
		weekday_list = get_weekday_list()
		return render(request, "toy/write_report.html", {"weekday_list": weekday_list})

	def post(self, request):
		weekday_list = get_weekday_list()
		id = request.POST.get("id")
		password = request.POST.get("password")

		with requests.Session() as session:
			
