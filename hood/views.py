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


@login_required(login_url='/accounts/login/')
def index(request):
    """
    View function that displays the home page and its contents
    """
    post = Post.objects.all()
    public = Social_Amenities.objects.all()
    return render(request, 'all/index.html', {"post": post, "public": public})


@login_required(login_url='/accounts/login/')
def search_results(request):
    """
    View function that enables a user to search for listed business
    """
    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_by_business_name(search_term)
        message = f"{search_term}"

        return render(request, 'all/search.html', {"message": message, "searched_businesses": searched_businesses})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all/search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def new_post(request):
    """
    View function that lets a user post up on the notice board
    """
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            return redirect('homepage')
    else:
        form = NewPostForm()
    return render(request, 'all/post.html', {"form": form})


@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    """
    View function that displays a user's profile
    """
    current_user = request.user
    profiles = Profile.objects.filter(user__id__iexact=profile_id)
    profile = Profile.objects.get(user=profile_id)
    all_profile = Profile.objects.all()
    content = {
        "profiles": profiles,
        "profile": profile,
        "user": current_user,
        "profile_id": profile_id,
        "all_profile": all_profile
    }
    return render(request, "all/profile.html", content)


@login_required(login_url='/accounts/login/')
def edit(request):
    """
    View function that lets a user edit their profile
    """
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            current_user = request.user
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile', current_user.id)
    else:
        form = EditProfileForm()
    return render(request, 'all/editprofile.html', {"form": form})


@login_required(login_url='/accounts/login/')
def business(request):
    """
    View function that lets a user create a business
    """
    current_user = request.user
    if request.method == 'POST':
        form = NewBusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.save()
            return redirect('homepage')
    else:
        form = NewBusinessForm()
    return render(request, 'all/business.html', {"form": form})


@login_required(login_url='/accounts/login/')
def social_amenities(request):
    """
    View function that lets a user create a social place or activity of an area
    """
    current_user = request.user
    if request.method == 'POST':
        form = NewSocialForm(request.POST)
        if form.is_valid():
            social = form.save(commit=False)
            social.user = current_user
            social.save()
            return redirect('homepage')
    else:
        form = NewSocialForm()
    return render(request, 'all/social_amenities.html', {"form": form})


@login_required(login_url='/accounts/login/')
def neighbourhood(request):
    """
    View function that lets a user create a new neighbourhood
    """
    current_user = request.user
    if request.method == 'POST':
        form = NewHoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user = current_user
            hood.save()
            return redirect('homepage')
    else:
        form = NewHoodForm()
    return render(request, 'all/hood.html', {"form": form})


@login_required(login_url='/accounts/login/')
def bizdisplay(request):
    """
    View function that displays all listed businesses
    """
    biz = Business.objects.all()
    return render(request, 'all/bizdisplay.html', {"biz": biz})


@login_required(login_url='/accounts/login/')
def hooddisplay(request):
    """
    View function that displays all listed neighbourhoods
    """
    hoods = Hood.objects.all()
    return render(request, 'all/displayhood.html', {"hoods": hoods})


def join(request, hoodId):
    """
    View function that lets new users join a specified neighbourhood 
    """
    neighbourhood = Hood.objects.get(pk=hoodId)
    if Join.objects.filter(user_id=request.user).exists():
        messages.success(
            request, 'Welcome. You are now a member of this Neighbourhood')
        Join.objects.filter(user_id=request.user).update(hood_id=neighbourhood)
        return redirect('displayhood')
    else:
        messages.success(
            request, 'Welcome. You are now a member of this Neighbourhood')
        Join(user_id=request.user, hood_id=neighbourhood).save()
        return redirect('displayhood')

def exitHood(request, hoodId):
	"""
	View function to delete a user from a neighbourhood
	"""
	if Join.objects.filter(user_id=request.user).exists():
		Join.objects.get(user_id=request.user).delete()

		return redirect('homepage')