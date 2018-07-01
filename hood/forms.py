from django import forms
from .models import Hood, Profile, Business, Post, Social_Amenities
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import TextInput, PasswordInput



class SignUpForm(UserCreationForm):
    """
    Class that creates a Sign up form
    """
    email = forms.EmailField(max_length=250)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ' Username'
        self.fields['email'].widget.attrs['placeholder'] = ' Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your Password'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        unique_together = ('email')

class LoginForm(AuthenticationForm):
    """
    class that creates a Login form
    """
    username = forms.CharField(widget=TextInput(attrs={'class':'validate', 'placeholder':'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class NewPostForm(forms.ModelForm):
    """
    class that creates a post form
    """
    class Meta:
        model = Post
        exclude = ['hood', 'user']
        

class EditProfile(forms.ModelForm):
    """
    class that lets a user edit their profile
    """
    class Meta:
        model = Profile
        exclude = ['user', 'email_confirmed']

class NewBusinessForm(forms.ModelForm):
    """
    class that let's a user fill in business information
    """
    class Meta:
        model = Business
        exclude = ['hood', 'user']

class NewHoodForm(forms.ModelForm):
    """
    class that let's a user fill in their neighbourhood details
    """
    class Meta:
        model = Hood
        fields = ('hoodName', 'hoodLocation', 'occupantsCount', 'admin')
        
class NewSocialForm(forms.ModelForm):
    """
    class that lets a user post information on social amenities
    """
    class Meta:
        model = Social_Amenities
        exclude = ['hood']
