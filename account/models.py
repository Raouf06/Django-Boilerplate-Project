from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
	def create_user(self,email,username,first_name,last_name,password=None):
		if not email:
			raise ValueError("Users must have a email")
		if not username:
			raise ValueError("Users must have a username")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			first_name=first_name,
			last_name=last_name,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password,first_name,last_name):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			first_name=first_name,
			last_name=last_name,
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	first_name = models.CharField(max_length=80)
	last_name = models.CharField(max_length=80)
	date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self,app_label):
		return True