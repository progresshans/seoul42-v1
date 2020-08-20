from django.db import models


class FtCursus(models.Model):
	CURSUS_TYPE = (
		('piscine', '피신'),
		('main', '본과'),
	)
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=20, blank=True, null=True)
	slug = models.CharField(max_length=20, blank=True, null=True)
	type = models.CharField(max_length=7, choices=CURSUS_TYPE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class FtProject(models.Model):
	PROJECT_TYPE = (
		('assignment', '과제'),
		('rush', '러쉬'),
		('exam', '시험'),
	)
	id = models.IntegerField(primary_key=True)
	type = models.CharField(max_length=10, choices=PROJECT_TYPE)
	name = models.CharField(max_length=50)
	slug = models.CharField(max_length=50)
	ft_cursus = models.ForeignKey(FtCursus, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class FtUserProject(models.Model):
	id = models.IntegerField(primary_key=True)
	ft_project = models.ForeignKey(FtProject, on_delete=models.CASCADE)
	occurrence = models.IntegerField(verbose_name="시도횟수")
	final_mark = models.IntegerField(verbose_name="최종점수")
	status = models.CharField(verbose_name="상태", max_length=15)
	is_pass = models.BooleanField(verbose_name="통과여부", default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class FtPool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20, blank=True, null=True)
	month = models.CharField(max_length=15)
	year = models.CharField(max_length=10)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Coalition(models.Model):
	id = models.IntegerField(unique=True, primary_key=True)
	name = models.CharField(verbose_name="길드 이름", max_length=50)
	color = models.CharField(verbose_name="길드 색상", max_length=7)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class FtUser(models.Model):
	id = models.IntegerField()
	email = models.EmailField(verbose_name="이메일")
	login = models.CharField(verbose_name="로그인 아이디", max_length=30, primary_key=True)
	image_url = models.URLField(verbose_name="프로필사진")
	is_ft_staff = models.BooleanField(verbose_name="스태프여부")
	ft_pool = models.ForeignKey(FtPool, on_delete=models.CASCADE)
	piscine_level = models.DecimalField(verbose_name="피신 레벨", max_digits=4, decimal_places=2)
	main_level = models.DecimalField(verbose_name="본과 레벨", max_digits=4, decimal_places=2, blank=True, null=True)
	is_piscine_pass = models.BooleanField(verbose_name="피신통과여부", default=False)
	correction_point = models.IntegerField(verbose_name="평가포인트")
	wallet = models.IntegerField(verbose_name="월렛포인트")
	location = models.CharField(verbose_name="위치", blank=True, null=True)
	now_cursus = models.ForeignKey(FtCursus, verbose_name="현재과정", blank=True, null=True, on_delete=models.CASCADE)
	coalition = models.ForeignKey(Coalition, verbose_name="길드", on_delete=models.CASCADE, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Tier(models.Model):
	FtUser = models.OneToOneField(FtUser, on_delete=models.CASCADE, primary_key=True)
	coalition_point = models.IntegerField(verbose_name="길드 포인트", blank=True, null=True)
	tier_name = models.CharField(verbose_name="티어 이름", max_length=13, blank=True, null=True)
	tier_rank = models.IntegerField(verbose_name="순위", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
