from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser, Profile, UserToken
from .forms import AdminChangeForm, AdminCreationForm


class UserAdmin(BaseUserAdmin):
	form = AdminChangeForm
	add_form = AdminCreationForm

	list_display = ('id', 'email', 'login', 'is_admin', 'is_active',)
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('id', 'login',)}),
		('Personal info', {'fields': ('email',)}),
		('Permissions', {'fields': ('is_admin', 'is_active',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('id', 'email', 'login', 'password1', 'password2',)}
		),
	)
	search_fields = ('login',)
	ordering = ('login',)
	filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(UserToken)
