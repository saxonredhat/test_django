from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import User,Role,Permission


class MyAuthBackend(ModelBackend):
	"""
	Use the login name and a hash of the password. For example:
	"""
	def authenticate(self, request, username=None, password=None):
		try:
			user = User.objects.get(Q(username=username)|Q(email=username))
		except User.DoesNotExist:
			return None
		else:
			if check_password(password, user.password) and self.user_can_authenticate(user):
				return user 
		return None 

	def user_can_authenticate(self, user):
		"""
		Reject users with is_active=False. Custom user models that don't have
		that attribute are allowed.
		"""
		is_active = getattr(user, 'is_active', None)
		return is_active or is_active is None
	

	def get_role_permissions(self, user_obj, obj=None):
		"""
		Return a set of permission strings the user `user_obj` has from the
		roles they belong.
		"""
		if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
			return set()

		perm_cache_name = '_role_perm_cache'
		if not hasattr(user_obj, perm_cache_name):
			if user_obj.is_superuser:
				perms = Permission.objects.all()
			else:
				user_roles_field = get_user_model()._meta.get_field('roles')
				user_roles_query = 'role__%s' % user_roles_field.related_query_name()
				perms = Permission.objects.filter(**{user_roles_query: user_obj})
			perms = perms.values_list('codename',).order_by()
			setattr(user_obj, perm_cache_name, {"%s" % name for name in perms})
		return getattr(user_obj, perm_cache_name)

	def get_all_permissions(self, user_obj, obj=None):
		if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
			return set()
		if not hasattr(user_obj, '_perm_cache'):
			user_obj._perm_cache = {
				*self.get_role_permissions(user_obj),
			}
		return user_obj._perm_cache

	def has_perm(self, user_obj, perm, obj=None):
		return user_obj.is_active and perm in self.get_all_permissions(user_obj, obj)

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None 
