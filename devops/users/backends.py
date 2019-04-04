from django.conf import settings
from django.contrib.auth.hashers import check_password
from .models import User


class MyAuthBackend:
	"""
	Use the login name and a hash of the password. For example:
	"""
	def authenticate(self, request, username=None, password=None):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return None
		else:
			if user.password == password and self.user_can_authenticate(user):
				return user 
		return None 

	def user_can_authenticate(self, user):
		"""
		Reject users with is_active=False. Custom user models that don't have
		that attribute are allowed.
		"""
		is_active = getattr(user, 'is_active', None)
		return is_active or is_active is None


	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None 
