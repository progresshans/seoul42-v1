from django import forms
from .models import Club, ClubMember


class ClubForm(forms.ModelForm):
	class Meta:
		model = Club
		fields = ('name', 'content', 'can_join',)
		widgets = {
			'name': forms.TextInput(attrs={
				'name': 'name_field',
				'class': 'form-control input-group'
			}),
			'content': forms.Textarea(attrs={
				'name': 'content_field',
				'class': 'form-control input-group'
			}),
			'can_join': forms.CheckboxInput(attrs={
				'name': 'can_join_field',
				'class': 'form-check-input',
				'checked': 'checked'
			}),
		}
		labels = {
			'name': '소모임 이름',
			'content': '소모임 소개',
			'can_join': '가입 가능하게 하기',
		}
