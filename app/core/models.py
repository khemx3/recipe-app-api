from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

import datetime


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""

    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('-', '-')
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    weight = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='-')
    birth = models.DateField(default=datetime.date.today)
    goal = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date = models.DateField()
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.date
