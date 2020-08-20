from django.contrib import admin
from .models import FtUser, Coalition, Tier, ApiKey


admin.site.register(FtUser)
admin.site.register(Tier)
admin.site.register(Coalition)
admin.site.register(ApiKey)