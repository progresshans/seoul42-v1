from django.shortcuts import render, reverse
from django.views.generic.base import TemplateView
from django.views import View
from .custom import get_random_string, authenticating_ft_api
from django.conf import settings
from django.contrib.auth import login, authenticate
from .models import MyUser


class SignInPage(TemplateView):
	template_name = "account/sign_in.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ft_api_state = get_random_string(21)
		self.request.session['ft_api_state'] = ft_api_state
		ft_api_sign_in = "https://api.intra.42.fr/oauth/authorize"
		redirect_uri = ""
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
			return render(request, "account/sign_in_error.html", {"task": "로그인 에러입니다. 다시 시도하세요."})
		else:
			ft_auth_api, ft_user_data = authenticating_ft_api(request.GET.get('code'), reverse('ft-login'))
			request.session['login_user'] = ft_user_data["login"]
			user = authenticate(request=request, login=ft_user_data["login"])
			if user:
				login(request, user)
			else:
				user = MyUser.objects.create_user(
					id=ft_user_data["id"],
					email=ft_user_data["email"],
					login=ft_user_data["login"],
				)
				login(request, user)
