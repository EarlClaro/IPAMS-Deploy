from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from records.models import Record
from django.db import models
from django.utils import timezone
from records.models import Subscription

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class UserRole(models.Model):
	name = models.CharField(max_length=100)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default='', blank=True)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=60, unique=True)
    contact_no = models.CharField(max_length=20, blank=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, default=7)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    subscription_status = models.CharField(max_length=60, default='unpaid', blank=True)
    is_subscribed = models.BooleanField(default=False)  # New field
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # def save(self, *args, **kwargs):
    #     # Ensure the save method logic does not conflict with subscription verification
    #     if self.role_id >= 3 and not self.is_subscribed:
    #         self.is_subscribed = True
    #         self.subscription_status = 'admin privilege'
    #     elif self.role_id < 3 and self.is_subscribed:
    #         self.is_subscribed = False
    #         self.subscription_status = 'unpaid'
    #     super(User, self).save(*args, **kwargs)

    def setUsername(self, username):
        self.username = username

    def setFirstName(self, firstName):
        self.firstName = firstName

    def setMiddleName(self, middleName):
        self.middleName = middleName

    def setEmail(self, email):
        self.email = email

    def setContactNo(self, contactNo):
        self.contact_no = contactNo

    def get_subscription(self):
        try:
            return self.subscription_set.get(status='active')
        except Subscription.DoesNotExist:
            return None

class College(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=10, default=None)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=10, default=None)
	college = models.ForeignKey(College, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Course(models.Model): #Program
	name = models.CharField(max_length=255, unique=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True, null=False, blank=True) 
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"

class RoleRequest(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
	date_requested = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username

class UserRecord(models.Model):
	record = models.ForeignKey(Record, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username + " - " + self.record.title

class Log(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	action = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.action

class Setting(models.Model):
	set_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
	name = models.CharField(max_length=100)
	value = RichTextField(blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	date_updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return self.name

class Adviser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	college = models.ForeignKey(College, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username