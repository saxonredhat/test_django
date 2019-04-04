from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.

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
	


class User(AbstractUser):
	username = models.CharField(max_length=100,unique=True)
	password = models.CharField(max_length=200)
	email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
	phone = models.CharField(verbose_name='phone',blank=True,max_length=11)
	is_active = models.BooleanField(default=False,verbose_name='is_active') 
	is_superuser = models.BooleanField(default=False)


	objects = MyUserManager()

	USERNAME_FIELD = 'username'

	REQUIRED_FIELDS = ['email']
	
	def get_full_name(self):
		return self.username
	
	def get_short_name(self):
		return self.username

	def __unicode__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return True
	
	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		"""Is the user a member of staff?"""
		return self.is_superuser


class Publisher(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=60)
	state_province = models.CharField(max_length=30)
	country = models.CharField(max_length=50)
	website = models.URLField()

	class Meta:
		ordering = ["-name"]

	def __str__(self):			  # __unicode__ on Python 2
		return self.name

class Author(models.Model):
	salutation = models.CharField(max_length=10)
	name = models.CharField(max_length=200)
	email = models.EmailField()
	headshot = models.ImageField(upload_to='author_headshots')
	last_accessed = models.DateTimeField()
	created_by = models.ForeignKey(
		User, 
		on_delete=models.CASCADE,
	)

	def get_absolute_url(self):
		return reverse('author-detail',kwargs={'pk': self.pk})

	def __str__(self):			  # __unicode__ on Python 2
		return self.name

class Book(models.Model):
	title = models.CharField(max_length=100)
	authors = models.ManyToManyField('Author')
	publisher = models.ForeignKey(
		Publisher,
		on_delete=models.CASCADE,
	)
	publication_date = models.DateField()
