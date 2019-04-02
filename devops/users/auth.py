from django.conf import settings
from django.contrib.auth.hashers import check_password
from .models import User

class SettingsBackend(object):
	"""
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

	ADMIN_LOGIN = 'admin'
	ADMIN_PASSWORD = 'pbkdf2_sha256$29000$WAuh9F7L2Rvj/J.z1loLAQ$nggNqAv7md1lBnxidEjyxA.hF8cGca6PCFmQ5rp99EY'
    """
	def authendticate(self,username=None,password=None):
		login_valid = (settings.ADMIN_LOGIN == username)
		pwd_valid = check_password(password,settings.ADMIN_PASSWORD)	
		if login_valid and pwd_valid:
			try:
				user = User.objects.get(username=username)
			except User.DoesNotExist:
				user=User(username=username)
				user.save()
			return user
		return None

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
