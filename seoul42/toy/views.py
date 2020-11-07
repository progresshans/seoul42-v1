import requests
from bs4 import BeautifulSoup as bs

from django.shortcuts import render
from django.views import View

from .utils import get_weekday_list, change_report_date


class WriteReport(View):
	def get(self, request):
		weekday_list = get_weekday_list()
		return render(request, "toy/write_report.html", {"weekday_list": weekday_list})

	def post(self, request):
		weekday_list, weekday_numbers = get_weekday_list(list(map(int, request.POST.getlist("weekday_select"))))
		login_info = {
			"user_name": request.POST.get("user_name"),
			"password": request.POST.get("password"),
		}

		with requests.Session() as s:
			login_page = s.get("http://git.innovationacademy.kr/user/login?redirect_to=")
			login_page_soup = bs(login_page.text, 'html.parser')
			csrf = login_page_soup.find('input', {'name': '_csrf'})
			login_info = {**login_info, **{'_csrf': csrf['value']}}
			login_result = s.post("http://git.innovationacademy.kr/user/login", data=login_info)

			report_page = s.get(f"http://git.innovationacademy.kr/{login_info['user_name']}/report/wiki/_pages")
			if report_page.status_code != 200:
				return render(request, "toy/toy_result.html", {"result": "로그인 에러"})
			report_page_soup = bs(report_page.text, 'html.parser')

			wiki_last_url = f'http://git.innovationacademy.kr{report_page_soup.select("body > div > div.repository.wiki.pages > div.ui.container > table > tbody > tr:nth-last-child(1) > td:nth-child(1) > a")[0]["href"]}/_edit'

			wiki_last = s.get(wiki_last_url)
			wiki_last_soup = bs(wiki_last.text, 'html.parser')
			wiki_text = wiki_last_soup.find('textarea', {'name': 'content'}).text

			wiki_new_url = f'http://git.innovationacademy.kr/{login_info["user_name"]}/report/wiki/_new'
			wiki_new = s.get(wiki_new_url)
			wiki_new_soup = bs(wiki_new.text, 'html.parser')
			csrf = wiki_new_soup.find('input', {'name': '_csrf'})

			for i in weekday_numbers:
				wiki_new_result = s.post(wiki_new_url, data={
					"title": weekday_list[i]['head'],
					"content": change_report_date(wiki_text, weekday_list[i]['head'], weekday_list[i]['body']),
					"_csrf": csrf['value'],
				})

		return render(request, "toy/toy_result.html", {"result": "보고서 작성 완료"})
