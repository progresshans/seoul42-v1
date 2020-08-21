from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RankSerializer
from .models import Tier


class RankListApi(APIView):
	def get(self, request):
		queryset = Tier.objects.all()
		serializer = RankSerializer(queryset, many=True)
		return Response(serializer.data)


class RankDetailApi(APIView):
	def get_object(self, login):
		try:
			return Tier.objects.get(FtUser__login=login)
		except:
			raise Http404

	def get(self, request, login):
		user = self.get_object(login)
		serializer = RankSerializer(user)
		return Response(serializer.data)
