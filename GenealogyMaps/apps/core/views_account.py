import jwt
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseBadRequest
from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.dispatch import Signal
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


from . import validators
from .models import UserProfile

class OwnUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=_("Imię"))
    last_name = forms.CharField(label=_("Nazwisko"))

    #def save(self, commit=True):
    #    user = super(UserCreationForm, self).save(commit)
    #    user.profile.first_name =

from django.contrib.auth import authenticate, get_user_model, login
from django.urls import reverse_lazy

User = get_user_model()

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


signals_user_registered = Signal(providing_args=["user", "request"])
user_activated = Signal(providing_args=["user", "request"])


class RegistrationForm(UserCreationForm):
    """
    Form for registering a new user account.
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    Subclasses should feel free to add any additional validation they
    need, but should take care when overriding ``save()`` to respect
    the ``commit=False`` argument, as several registration workflows
    will make use of it to create inactive user accounts.
    """
    class Meta(UserCreationForm.Meta):
        fields = [
            #User.USERNAME_FIELD,
            User.get_email_field_name(),
            'password1',
            'password2',
            'first_name',
            'last_name',
            'parishes',
            'lastnames'
        ]

    parishes = forms.CharField(label='Parafie którymi się interesuję', widget=forms.Textarea)
    lastnames = forms.CharField(label='Nazwiska których szukam', widget=forms.Textarea)

    error_css_class = 'error'
    required_css_class = 'required'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email=email)
        if len(users) > 0:
            raise forms.ValidationError(
                'Konto już istnieje',
                code='email_exists',
            )
        return email

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        email_field = User.get_email_field_name()
        if hasattr(self, 'reserved_names'):
            reserved_names = self.reserved_names
        else:
            reserved_names = validators.DEFAULT_RESERVED_NAMES

        self.fields[email_field].validators.append(
            validators.validate_confusables_email
        )
        self.fields[email_field].required = True

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['parishes'].required = True
        self.fields['lastnames'].required = True


class BaseRegistrationView(FormView):
    """
    Base class for user registration views.
    """
    disallowed_url = reverse_lazy('registration_disallowed')
    form_class = RegistrationForm
    success_url = None
    template_name = 'django_registration/registration_form.html'

    def dispatch(self, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        """
        if not self.registration_allowed():
            return HttpResponseRedirect(force_text(self.disallowed_url))
        return super(BaseRegistrationView, self).dispatch(*args, **kwargs)

    def get_success_url(self, user=None):
        """
        Return the URL to redirect to after successful redirection.
        """
        # This is overridden solely to allow django-registration to
        # support passing the user account as an argument; otherwise,
        # the base FormMixin implementation, which accepts no
        # arguments, could be called and end up raising a TypeError.
        return super(BaseRegistrationView, self).get_success_url()

    def form_valid(self, form):
        return HttpResponseRedirect(
            self.get_success_url(self.register(form))
        )

    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def register(self, form):
        """
        Implement user-registration logic here. Access to both the
        request and the registration form is available here.
        """
        raise NotImplementedError


class RegistrationView(BaseRegistrationView):
    """
    Registration via the simplest possible process: a user supplies a
    username, email address and password (the bare minimum for a
    useful account), and is immediately signed up and logged in.
    """
    success_url = reverse_lazy('registration_complete')

    def register(self, form):
        try:
            new_user = form.save(commit=False)
            new_user.username = new_user.email
            new_user.is_active = False
            new_user.save()

            up = UserProfile.objects.create(user=new_user)
            up.parishes = form.cleaned_data['parishes']
            up.lastnames = form.cleaned_data['lastnames']
            up.save()
    
            #new_user = authenticate(**{
            #    User.USERNAME_FIELD: new_user.get_username(),
            #    'password': form.cleaned_data['password1']
            #})
            # login(self.request, new_user)
            signals_user_registered.send(
                sender=self.__class__,
                user=new_user,
                request=self.request
            )
            return new_user
        except:
            return None


def after_registration(sender, user, request, **kwargs):
    # mail d admina
    subject = '[katalog] Nowe konto'
    url = 'https://katalog.projektpodlasie.pl/a/users'
    message = u'Nowe konto do akceptacji %s %s.\n%s' % (user.first_name, user.last_name, url, )
    for stf in User.objects.filter(is_staff=True):
        send_mail(subject, message, 'info@parafie.k37.ovh', (stf.email,) )


signals_user_registered.connect(after_registration)


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            print('!!!', user.is_active)
            raise forms.ValidationError(
                _("Konto czeka na aktywację przez administratora."),
                code='inactive',
            )

@csrf_exempt
def sso(request):
    ssoJwt = request.POST.get('ssoJwt', None)

    try:
        token = jwt.decode(ssoJwt, settings.JWT_SECRET, audience=settings.JWT_AUD, algorithms=[settings.JWT_ALGO])
        #token_data = json.loads(token)
    except Exception as e:
        token = None
        raise HttpResponseBadRequest('Invalid request.')

    email = token['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User()
        user.username = email
        user.email = email
        # skoro jest zalogowany na indexach to zakladamy, ze tam konto jest juz potwierdzone
        user.is_active = True
        user.save()

    login(request, user)
    return HttpResponseRedirect('/')

    #data = {
    #    'token': token
    #}
    #return JsonResponse(data)
