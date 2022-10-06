from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField, EmailField, IntegerField, BooleanField, URLField
from django.core.validators import RegexValidator
from user.managers import CustomUserManager
# Create your models here.


class Users(AbstractUser):
    """
    User Details
    """
    firebase = CharField('firebaseID', max_length=128, null=False, unique=True,
                         primary_key=True, blank=False)

    # username = CharField('username', max_length=255, null=False, unique=True,
    #                      blank=False)
    name = CharField('username', max_length=255, null=False, unique=True,
                         blank=False)
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = CharField('phone', max_length=13, null=False, unique=False)
    ChatReports = IntegerField('ChatReports', default=0)
    ChatAllowed = BooleanField('ChatAllowed', default=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    email = EmailField('email', unique=True)
    score = IntegerField('score', default=0)
    instagramId = CharField(
        'instagramId', max_length=255, blank=True, null=True)
    profileImage = URLField(
        'profileImage', max_length=255, null=True, blank=True)
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
        ('D', 'DonotDisclose'),
    )

    gender = CharField(max_length=1, choices=GENDER_CHOICES)
    username = None
    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


    def __str__(self) -> str:
        return self.name
