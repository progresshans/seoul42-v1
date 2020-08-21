from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import RankSerializer
from .models import Tier


# class RankListApi(APIView):
# 	def get(self, request):
# 		queryset = Tier.objects.all()
# 		serializer = RankSerializer(queryset, many=True)
# 		return Response(serializer.data)
#
#
# class RankDetailApi(APIView):
# 	def get_object(self, login):
# 		try:
# 			return Tier.objects.get(FtUser__login=login)
# 		except:
# 			raise Http404
#
# 	def get(self, request, login):
# 		user = self.get_object(login)
# 		serializer = RankSerializer(user)
# 		return Response(serializer.data)


class RankApi(ReadOnlyModelViewSet):
	"""
	카뎃 Ranking 전체 데이터 API
	---
	카뎃의 데이터를 바탕으로 Seoul42에서 롤식 랭킹을 부여한 전체 데이터를 가져올 수 있습니다.
	"""
	queryset = Tier.objects.all()
	serializer_class = RankSerializer

	param_login_hint = openapi.Parameter(
		'login',
		openapi.IN_PATH,
		description="42 Intra에 login할때 사용하는 아이디입니다. ex) 'hhan'",
		type=openapi.TYPE_STRING
	)

	@swagger_auto_schema(
		manual_parameters=[param_login_hint],
		responses={

		}
	)

	def retrieve(self, request, login=None, **kwargs):
		"""
		카뎃 Ranking 개별 데이터 API
		---
		카뎃의 데이터를 바탕으로 Seoul42에서 롤식 랭킹을 부여한 개별 데이터를 가져올 수 있습니다.
		"""
		queryset = Tier.objects.all()
		user = get_object_or_404(queryset, FtUser__login=login)
		serializer = RankSerializer(user)
		return Response(serializer.data)
