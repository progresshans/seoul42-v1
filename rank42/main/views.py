from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views import View

from .rank import RankTier
from .models import FtUser


class Main(View):
	"""
	메인페이지
	"""
	def get(self, request, **kwargs):
		if request.GET.get('login'):
			return redirect('search', login=request.GET.get('login'))
		return render(request, "main/main.html")


class List(TemplateView):
	"""
	Rank42의 본과정 학생들 전체 랭킹 페이지
	"""
	template_name = "main/list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ft_users = FtUser.objects.filter(is_alive=True).exclude(coalition_point=0).order_by('-coalition_point')
		unrank_ft_users = FtUser.objects.filter(is_alive=True, coalition_point=0)
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
		for temp_user in ft_users:
			if temp_user.tier.tier_name != ft_user.tier.tier_name:
				return temp_user.tier.tier_name, temp_user.tier.coalition_point - ft_user.tier.coalition_point
		return 0, 0

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		login = kwargs['login']
		ft_users = FtUser.objects.filter(is_alive=True).order_by('-coalition_point')
		ft_user = ft_users.get(login=login)
		ft_user.percent = round((ft_user.tier.tier_rank / ft_users.count()) * 100, 1)
		if ft_user.tier.coalition_point != 0:
			ft_user.next_tier_name, ft_user.next_tier_point = self.get_next_tier_name(reversed(list(ft_users[:ft_user.tier.tier_rank - 1])), ft_user)
			ft_user.need_peer_evaluation = (ft_user.next_tier_point // 42) + 1
			ft_user.tier_img = RankTier().get_tier_img(ft_user.tier.tier_name)
		else:
			ft_user.next_tier_name, ft_user.next_tier_point = -1, -1

		context['ft_user'] = ft_user
		return context