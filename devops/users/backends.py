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
			if user.password == password:
				return user 
		except User.DoesNotExist:
			return None
		return None 

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None 
