from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import SignUpForm, EditProfileForm, LoginForm, NewBusinessForm, NewHoodForm, NewPostForm, NewSocialForm
import json
# import request
from .models import Hood, Profile, Post, Business, save_user_profile, Join, Social_Amenities
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
# from googlemaps import Client, convert
from django.conf import settings
# from .decorators import user_belongs_to_hood
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages




# Create your views here.
def signup(request):
    """
    View function that ensures a user is first authenticated prior using/accesing the application.
    """
    current_user = request.user
    if current_user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Neighbourhood Watch Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    """
    View function that sends out an activation email to a user
    """
    current_user = request.user
    if current_user.is_authenticated():
        return HttpResponseRedirect('/')
    return render(request, 'registration/activation_complete.html')


def activate(request, uidb64, token):
    """
    View funtion that activates their account once they signup to use the application
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('logout')
    else:
        return render(request, 'registration/account_activation_invalid.html')

