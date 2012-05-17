from django import forms
from django.core import validators
from django.contrib.auth.models import User
 
class RegistrationForm(forms.Form):
	_errors = {}
	error_class = []
	def __init__(self):
		username = forms.CharField(label='username',
				max_length=30,
				required=True, validators=[validators.RegexValidator(r"^(\w\d-_@)+$", "Username must be alphanumeric"),
					self.isValidUsername]),
		email = forms.EmailField(label='email',
			    max_length=30,
			    required=True),
		password1 = forms.CharField(label='password1',
				widget=forms.PasswordInput,
				max_length=60,
				required=True),
		password2 = forms.CharField(label='password2',
				widget=forms.PasswordInput,
				max_length=60,
				required=True,
				validators=[self.PasswordMatch]),
			     
	def isValidUsername(self, field_data, all_data):
		try:
			User.objects.get(username=field_data)
		except User.DoesNotExist:
			return
		raise validators.ValidationError({'username': ['The username "%s" is already taken.' % field_data, ]})
		self._errors['username'].append('The username "%s" is already taken.' % field_data)

	def PasswordMatch(self, field_data, all_data):
		if field_data != all_data['password1']:
			raise validators.ValidationError({'passwords': ["Passwords must match", ]});
			self._errors['passwords'].append('Passwords must match')
		else:
			return
																	     
	def save(self, new_data):
		u = User.objects.create_user(new_data['username'],
			new_data['email'],
			new_data['password1'])
		u.is_active = False
		u.save()
		return u
