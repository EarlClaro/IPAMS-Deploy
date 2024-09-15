from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True , max_length=30)
    name = models.CharField(max_length=255, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
        
    def get_full_name(self):
        return self.name

# research paper model
class researchpaper(models.Model):
    title = models.CharField(max_length=100)
    abstract = models.TextField()
    year = models.CharField(max_length=30)
    record_type_id = models.BigIntegerField(null=True)
    adviser_id = models.BigIntegerField(null=True)
    classification_id = models.BigIntegerField()
    representative = models.CharField(max_length=100)
    year_accomplished = models.CharField(max_length=30)
    year_completed = models.CharField(max_length=30, null=True)
    is_ip = models.BooleanField()
    for_commercialization = models.BooleanField()
    date_created = models.DateTimeField()
    is_marked = models.BooleanField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'backend_researchpaper'





class Thread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    thread_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)