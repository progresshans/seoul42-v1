from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View

from .rank import RankTier, get_tier_img
from .models import FtUser, Coalition
from .ftapi import FtApi

from account.models import MyUser, Profile


class Main(View):
	"""
	메인페이지
	"""
	def get(self, request, **kwargs):
		if request.GET.get('login'):
			if request.GET.get('login') == "피신랭킹이너무보고싶어요":
				user = MyUser.objects.get(login=request.user.login)
				user.allow_piscine_list = True
				user.save()
				return render(request, "main/print_message.html", {"message": "뾰로롱~ 보세요!"})
			elif request.GET.get('login') == "25만원받고싶어":
				return redirect('write_report')
			else:
				return redirect('search', login=request.GET.get('login'))
		return render(request, "main/main.html")


class List(TemplateView):
	"""
	Rank42의 본과정 학생들 전체 랭킹 페이지
	"""
	template_name = "main/list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# 유저 모델을 불러와서 랭크 티어를 다시 지정함
		ft_users = FtUser.objects.filter(is_alive=True).exclude(tier__coalition_point=0).order_by(
			"-tier__coalition_point")
		unrank_ft_users = FtUser.objects.filter(is_alive=True, tier__coalition_point=0)
		rank_tier = RankTier(ft_users.count())

		context['ft_users'], context['unrank_ft_users'] = rank_tier.set_tier(ft_users, unrank_ft_users)
		return context


class Search(TemplateView):
	"""
	특정 유저의 랭킹 및 자세한 정보를 보여주는 페이지
	"""
	template_name = "main/search.html"

	@staticmethod
	def get_next_tier_name(ft_users, ft_user):
		"""
		현재 유저의 티어에서 바로 다음 티어의 이름과 필요한 점수를 찾아서 리턴

		:param ft_users: ft_user를 기준으로 뒤집어진 유저 모델 리스트
		:param ft_user: 현재 유저
		:return: (다음 티어 이름, 다음 티어까지 필요한 점수), 다음 티어가 안 존재하면 (0,0) 리턴
		"""
		for temp_user in ft_users:
			if temp_user.tier.tier_name != ft_user.tier.tier_name:
				return temp_user.tier.tier_name, temp_user.tier.coalition_point - ft_user.tier.coalition_point
		return 0, 0

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		login = kwargs['login']
		ft_users = FtUser.objects.filter(is_alive=True).order_by('-tier__coalition_point')
		ft_user = ft_users.get(login=str(login))
		ft_user.percent = round((ft_user.tier.tier_rank / ft_users.count()) * 100, 1)
		if ft_user.tier.coalition_point != 0:
			ft_user.next_tier_name, ft_user.next_tier_point = self.get_next_tier_name(
				reversed(list(ft_users[:ft_user.tier.tier_rank - 1])),
				ft_user,
			)
			ft_user.need_peer_evaluation = (ft_user.next_tier_point // 42) + 1
			ft_user.tier_img = get_tier_img(ft_user.tier.tier_name)
		else:
			ft_user.next_tier_name, ft_user.next_tier_point = -1, -1

		context['ft_user'] = ft_user
		return context


class UpdateFtUser(View):
	"""
	42 유저 업데이트
	"""
	def post(self, request):
		ft_api: FtApi = FtApi()
		ft_user = FtUser.objects.get(id=request.POST.get('id'))
		coalition_data = ft_api.get_data(url=f'users/{ft_user.id}/coalitions_users')
		if coalition_data and Coalition.objects.filter(id=int(coalition_data[0]["coalition_id"])).exists():
			ft_user.tier.coalition_point = coalition_data[0]["score"]
			ft_user.tier.save()
		else:
			ft_user.is_alive = False
			ft_user.save()
		ft_users = FtUser.objects.filter(is_alive=True).exclude(tier__coalition_point=0).order_by(
			'-tier__coalition_point')
		rank_tier = RankTier(ft_users.count())
		rank_tier.set_tier(ft_users)
		return redirect('search', login=ft_user.login)


class GithubRank(TemplateView):
	template_name = "main/github_rank.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		profiles = Profile.objects.all().exclude(github_login=None).order_by('-github_total_star')
		context['profiles'] = profiles
		return context
