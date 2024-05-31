from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError
from .managers import CustomUserManager
from django.contrib.auth import get_user_model
import re

class CustomUser(AbstractUser):
	username = None
	phone_number = models.CharField(max_length=15, unique=True, blank= False)
	email = models.EmailField(unique=True, blank=True, null=True)
	first_name = models.CharField(max_length=30, blank=False)
	last_name = models.CharField(max_length=30, blank=False)
	groups = models.ManyToManyField(Group, related_name='users', related_query_name='user')
	user_permissions = models.ManyToManyField(Permission, related_name='users', related_query_name='user')
	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = ['first_name', 'last_name']
	objects = CustomUserManager()
    
	def clean_phone_number(self):
		phone_number = self.phone_number
		if not re.match(r'^\+?1?\d{9,15}$', phone_number):
			raise ValidationError('Invalid phone number')
		return phone_number


class Contact(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	phone_number = models.CharField(max_length=20)
	email_address = models.EmailField()
	spam = models.BooleanField(default=False)

	@classmethod
	def search_by_name(cls, query):
		return cls.objects.filter(name__istartswith=query).union(
			cls.objects.filter(name__icontains=query).exclude(name__istartswith=query))
	@classmethod
	def search_by_phone_number(cls, query):
		contacts = cls.objects.filter(phone_number=query)
		user = get_user_model().objects.filter(phone_number=query).first()
		if user:
			contacts = contacts.union(cls.objects.filter(user=user))
		return contacts

	def get_details(self, user):
		details = {
			'name': self.name,
			'phone_number': self.phone_number,
			'spam_likelihood': self.spam,
		}
		if self.user == user and self.email_address:
			details['email_address'] = self.email_address
		return details
  

  
class SpamNumber(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

