import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail

from apps.users.models import UserProfile
from apps.users.forms import RegistrationForm

def register(request):
	if request.user.is_authenticated():
		# They already have an account; don't let them register again
		return render_to_response('user/register.html', {'has_account': True})
	manipulator = RegistrationForm()
	if request.POST:
		new_data = request.POST.copy()
		errors = manipulator.get_validation_errors(new_data)
		if not errors:
			# Save the user                                                                                                                                           	 
			manipulator.do_html2python(new_data)
			new_user = manipulator.save(new_data)
			# Build the activation key for their account                                                                                                                    
			salt = sha.new(str(random.random())).hexdigest()[:5]
			activation_key = sha.new(salt+new_user.username).hexdigest()
			key_expires = datetime.datetime.today() + datetime.timedelta(2)
			# Create and save their profile                                                                                                                                 
			new_profile = UserProfile(user=new_user,
			activation_key=activation_key,
			key_expires=key_expires)
			new_profile.save()
			# Send an email with the confirmation link                                                                                                                      
			email_subject = 'Your new example.com account confirmation'
			email_body = "Hello, %s, and thanks for signing up for an \                                                                                                     
						example.com account!\n\nTo activate your account, click this link within 48 \                                                                                               
						hours:\n\nhttp://example.com/accounts/confirm/%s" % (
							new_user.username,
							new_profile.activation_key)
			send_mail(email_subject,
				email_body,
				'accounts@example.com',
				[new_user.email])
			return render_to_response('user/register.html', {'created': True})
		else:
			errors = new_data = {}
			form = forms.FormWrapper(manipulator, new_data, errors)
		    return render_to_response('user/register.html', {'form': form})

def confirm(request, activation_key):
    if request.user.is_authenticated():
	    return render_to_response('user/confirm.html', {'has_account': True})
	user_profile = get_object_or_404(UserProfile,
		activation_key=activation_key)
	if user_profile.key_expires < datetime.datetime.today():
		return render_to_response('user/confirm.html', {'expired': True})
	user_account = user_profile.user
	user_account.is_active = True
	user_account.save()
	return render_to_response('user/confirm.html', {'success': True})

def login(request):
	if request.user.is_authenticated():
		return render_to_response('user/login', {
			'logged_in': True,
		})
	if request.POST:
		data = request.POST.copy()
		user = authenticate(username=data.username, password=data.password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render_to_response('user/login.html', {
					'success': True, 
				})
			else:
				return render_to_response('user/login.html', {
					'disabled': True,
				})
		else:
			return render_to_response('user/login.html', {
				'incorrect': True,
			})
	else:
		errors = data = {}
		form = LoginForm()
	return render_to_response('user/login.html', {
		'form': form,
	})
