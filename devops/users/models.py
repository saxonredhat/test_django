from django.db import models
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone



# Create your models here.
class Permission(models.Model):
	LEVEL_CHOICES=(
		(1,'一级'),
		(2,'二级'),
	)
	name = models.CharField(max_length=255, unique=True, verbose_name='权限名')
	codename = models.CharField(max_length=100, null=True, blank=True, verbose_name='权限代码')
	#level = models.IntegerField('level', choices=LEVEL_CHOICES,default=1)
	#parent_permission = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subpermissions')
	#seq = models.IntegerField('seq', default=0)
	comment = models.CharField(blank=True, max_length=500,verbose_name='描述')

	def __str__(self):
		return self.name

	def natural_key(self):
		return (self.name,)

	def get_absolute_url(self):
		return reverse('users:permission-list')	


class Role(models.Model):
	name = models.CharField(max_length=100, unique=True,verbose_name='角色名')
	permissions = models.ManyToManyField(
		Permission,
		blank=True,
		verbose_name='权限',
	)
	comment = models.CharField(blank=True, max_length=500,verbose_name='描述')

	def __str__(self):
		return self.name

	def natural_key(self):
		return (self.name,)

	def get_absolute_url(self):
		return reverse('users:role-detail', args=[str(self.id)])	

	@property
	def all_permissions(self):
		return ', '.join([p.name for p in self.permissions.all()])


class Department(models.Model):
	name = models.CharField(max_length=100, unique=True,verbose_name='部门名字')
	comment = models.CharField(blank=True, max_length=500,verbose_name='描述')

	def __str__(self):
		return self.name

	def natural_key(self):
		return (self.name,)

	def get_absolute_url(self):
		return reverse('users:department-detail', args=[str(self.id)])	


class Menu(models.Model):
	name = models.CharField('name', max_length=100, unique=True)
	url = models.CharField('url', null=True, blank=True, max_length=80)
	icon_name = models.CharField('icon_name', default='file', null=True, blank=True, max_length=20)
	parent_menu = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus') 
	is_topmenu = models.BooleanField(default=False,verbose_name='is_topmenu')
	comment = models.CharField(blank=True, max_length=500,verbose_name='描述')

	def __str__(self):
		return self.name

	def natural_key(self):
		return (self.name,)

	def get_absolute_url(self):
		return reverse('users:menu-detail', args=[str(self.id)])	


class MyUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):	
		if not username:
			raise ValueError('Users must have an username')
		if not email:
			raise ValueError('Users must have an email address')
		user = self.model(
			username=username,
			email=self.normalize_email(email),
		)
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, username, email, password):
		user = self.create_user(username,
			email=self.normalize_email(email),
			password=password,
		)
	
		user.is_superuser = True
		user.save(using=self._db)
		return user
	

def _user_has_perm(user, perm, obj):
	"""
	A backend can raise `PermissionDenied` to short-circuit permission checking.
	"""
	for backend in auth.get_backends():
		if not hasattr(backend, 'has_perm'):
			continue
		try:
			if backend.has_perm(user, perm, obj):
				return True
		except PermissionDenied:
			return False
	return False


def _user_get_all_permissions(user, obj):
	permissions = set()
	for backend in auth.get_backends():
		if hasattr(backend, "get_all_permissions"):
			permissions.update(backend.get_all_permissions(user, obj))
	return permissions


class MyPermissionsMixin(models.Model):
	"""
	Add the fields and methods necessary to support the Group and Permission
	models using the ModelBackend.
	"""
	is_superuser = models.BooleanField(
		_('超级管理员'),
		default=False,
		help_text=_(
			'Designates that this user has all permissions without '
			'explicitly assigning them.'
		),
	)
	roles = models.ManyToManyField(
		Role,
		verbose_name=_('角色'),
		blank=True,
		help_text=_(
			'The roles this user belongs to. A user will get all permissions '
			'granted to each of their roles.'
		),
		related_name="user_set",
		related_query_name="user",
	)

	class Meta:
		abstract = True

	def get_role_permissions(self, obj=None):
		"""
		Return a list of permission strings that this user has through their
		groups. Query all available auth backends. If an object is passed in,
		return only permissions matching this object.
		"""
		permissions = set()
		for backend in auth.get_backends():
			if hasattr(backend, "get_role_permissions"):
				permissions.update(backend.get_role_permissions(self, obj))
		return permissions

	def get_all_permissions(self, obj=None):
		return _user_get_all_permissions(self, obj)

	def has_perm(self, perm, obj=None):
		"""
		Return True if the user has the specified permission. Query all
		available auth backends, but return immediately if any backend returns
		True. Thus, a user who has permission from a single auth backend is
		assumed to have permission in general. If an object is provided, check
		permissions for that object.
		"""
		# Active superusers have all permissions.
		if self.is_active and self.is_superuser:
			return True

		# Otherwise we need to check the backends.
		return _user_has_perm(self, perm, obj)

	def has_perms(self, perm_list, obj=None):
		"""
		Return True if the user has each of the specified permissions. If
		object is passed, check if the user has all required perms for it.
		"""
		return all(self.has_perm(perm, obj) for perm in perm_list)

	def has_module_perms(self, app_label):
		return True



class MyAbstractUser(AbstractBaseUser, MyPermissionsMixin):
	"""
	An abstract base class implementing a fully featured User model with
	admin-compliant permissions.

	Username and password are required. Other fields are optional.
	"""
	username_validator = UnicodeUsernameValidator()

	username = models.CharField(
		_('用户名'),
		max_length=150,
		unique=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
	)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=150, blank=True)
	email = models.EmailField(_('邮箱'), max_length=150, unique=True,blank=False)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
		_('激活'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	objects = MyUserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
		abstract = True

	@property
	def full_name(self):
		return '{} {}'.format(self.first_name, self.last_name)

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def get_full_name(self):
		"""
		Return the first_name plus the last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		"""Return the short name for the user."""
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""Send an email to this user."""
		send_mail(subject, message, from_email, [self.email], **kwargs)


class User(MyAbstractUser):
	name = models.CharField(verbose_name='name',blank=True,max_length=11)
	phone = models.CharField(verbose_name='手机',blank=True,max_length=11)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='users',verbose_name='部门') 
	objects = MyUserManager()

	REQUIRED_FIELDS = ['email']
	

	def __unicode__(self):
		return self.username

	def get_absolute_url(self):
		return reverse('users:user-list')	

	@property
	def is_staff(self):
		"""Is the user a member of staff?"""
		return self.is_superuser

