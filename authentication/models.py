from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db.models import Q
from django.contrib.auth.models import (
	BaseUserManager,
	AbstractBaseUser
)
#from allauth.socialaccount.models import SocialAccount, SocialApp


# Create your models here.

class MobUserManager(BaseUserManager):
	
	def create_user(self, mob):
		user = self.model(mob=mob)
		user.save(using=self._db)
		return user

	def create_superuser(self, mob, password):
		user = self.model(mob=mob)
		user.set_password(password)
		user.is_admin = True
		user.save(using=self._db)
		return user

class MobUser(AbstractBaseUser):
	mob = models.CharField(max_length=20, unique=False, null=True, blank=True)
	USERNAME_FIELD = 'mob'
	create_time = models.DateTimeField(auto_now=True)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	objects = MobUserManager()

	def __unicode__(self):
		return '%s(%s)' % (self.mob, self.id)

	def get_full_name(self):
		return self.mob

	def get_short_name(self):
		return self.mob

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin

	@property
	def wx_socialaccounts(self):
		return self.socialaccount_set.filter(provider='weixin')

	@property
	def real_wx_extra_data(self):
		social_account = self.wx_socialaccounts.first()
		if social_account and hasattr(social_account, 'extra_data'):
			return social_account.extra_data
		return None

	@property
	def real_wx_nickname(self):
		extra_data = self.real_wx_extra_data
		if extra_data:
			return extra_data.get('nickname', None)
		return None

	@property
	def real_wx_headimgurl(self):
		extra_data = self.real_wx_extra_data
		if extra_data:
			return extra_data.get('headimgurl', None)
		return None

	def get_wx_extra_data(self, request):
		social_app = SocialApp.objects.get_current('weixin', request)
		social_account = self.wx_socialaccounts.filter(social_app=social_app).first()
		if social_account and hasattr(social_account, 'extra_data'):
			return social_account.extra_data
		return None

	def get_wx_openid(self, request):
		extra_data = self.get_wx_extra_data(request)
		if extra_data:
			return extra_data.get('openid', None)
		return None
