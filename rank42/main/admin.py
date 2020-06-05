from django.contrib import admin
from .models import FtUser, Coalition, Tier


admin.site.register(FtUser)
admin.site.register(Tier)
admin.site.register(Coalition)