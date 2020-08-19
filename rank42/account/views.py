import requests

from django.shortcuts import render, reverse, redirect
from django.views.generic.base import TemplateView
from django.views import View
from django.views.generic.edit import CreateView
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .custom import get_random_string, authenticating_ft_api
from .models import MyUser, Profile


class SignInPage(TemplateView):
	template_name = "account/sign_in.html"

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		ft_api_state = get_random_string(21)
		self.request.session['ft_api_state'] = ft_api_state
		ft_api_sign_in = "https://api.intra.42.fr/oauth/authorize"
		redirect_uri = f"{settings.AM_I_HTTPS}://{self.request.get_host()}{reverse('ft_login')}"
		response_type = "code"
		context['ft_api_sign_in_url'] = (
			f"{ft_api_sign_in}?"
			f"client_id={settings.FT_UID_KEY}&"
			f"redirect_uri={redirect_uri}&"
			f"response_type={response_type}&"
			f"state={ft_api_state}"
		)
		return context


class FtApiSignIn(View):
	def get(self, request):
		if request.session.get('ft_api_state') and not request.GET.get('state') == request.session['ft_api_state']:
			return render(request, "account/sign_in_error.html", {"error": "로그인 에러입니다. 다시 시도하세요."})
		else:
			ft_auth_api, ft_user_data = authenticating_ft_api(
				request.GET.get('code'),
				f"{settings.AM_I_HTTPS}://{self.request.get_host()}{reverse('ft_login')}",
			)
			print(f"code : {request.GET.get('code')}")
			print(f"gac : {ft_auth_api.get_access_token()}")
			if ft_auth_api is None:
				return render(request, "account/sign_in_error.html", {"error": "로그인 에러입니다. 다시 시도하세요."})
			request.session['login_user'] = ft_user_data["login"]
			user = authenticate(request=request, login=ft_user_data["login"])
			if user:
				login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
				return redirect('main')
			else:
				user = MyUser.objects.create_user(
					id=ft_user_data["id"],
					email=ft_user_data["email"],
					login=ft_user_data["login"],
				)
				user.usertoken.ft_token = ft_auth_api.get_refresh_token()
				user.usertoken.save()
				login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
				return redirect('main')


class LogOut(View):
	def post(self, request):
		logout(request)
		return redirect('main')


class MyPage(TemplateView):
	template_name = "account/mypage.html"


class AddGithubId(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, "account/add_github_id.html")

	def post(self, request):
		github_response = requests.get(f"https://api.github.com/users/{request.POST.get('id')}")
		if github_response.status_code == 200:
			github_response = github_response.json()
			profile = Profile.objects.get(user=request.user)
			profile.github_login = github_response["login"]
			profile.github_id = github_response["id"]
			profile.github_bio = github_response["bio"]
			profile.github_html_url = github_response["html_url"]
			profile.github_avatar_url = github_response["avatar_url"]
			profile.github_total_star = requests.get(f"https://api.github-star-counter.workers.dev/user/{request.POST.get('id')}").json()["stars"]
			profile.save()
			return redirect('mypage')
		else:
			return render(request, "account/add_github_id.html", {"error": "잘못된 Github ID입니다."})
