from rest_framework import serializers
from .models import Tier
from .rank import get_tier_img


class RankSerializer(serializers.ModelSerializer):
	id = serializers.SerializerMethodField()
	login = serializers.SerializerMethodField()
	coalition_id = serializers.SerializerMethodField()
	coalition_name = serializers.SerializerMethodField()
	coalition_color = serializers.SerializerMethodField()
	tier_img = serializers.SerializerMethodField()

	def get_id(self, obj):
		return obj.FtUser.id

	def get_login(self, obj):
		return obj.FtUser.login

	def get_coalition_id(self, obj):
		return obj.FtUser.coalition.id

	def get_coalition_name(self, obj):
		return obj.FtUser.coalition.name

	def get_coalition_color(self, obj):
		return obj.FtUser.coalition.color

	def get_tier_img(self, obj):
		return get_tier_img(obj.tier_name)

	class Meta:
		model = Tier
		fields = (
			'id',
			'login',
			'coalition_id',
			'coalition_name',
			'coalition_point',
			'coalition_color',
			'tier_name',
			'tier_rank',
			'tier_img',
			'updated_at',
		)
