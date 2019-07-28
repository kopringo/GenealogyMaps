from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.dispatch import Signal

from . import validators

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
            'last_name'
        ]

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        email_field = User.get_email_field_name()
        if hasattr(self, 'reserved_names'):
            reserved_names = self.reserved_names
        else:
            reserved_names = validators.DEFAULT_RESERVED_NAMES

        #username_validators = [
        #    validators.ReservedNameValidator(reserved_names),
        #    validators.validate_confusables
        #]
        #self.fields[User.USERNAME_FIELD].validators.extend(username_validators)

        self.fields[email_field].validators.append(
            validators.validate_confusables_email
        )
        self.fields[email_field].required = True

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

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
        new_user = form.save(commit=False)
        new_user.username = new_user.email
        new_user.save()

        new_user = authenticate(**{
            User.USERNAME_FIELD: new_user.get_username(),
            'password': form.cleaned_data['password1']
        })
        login(self.request, new_user)
        signals_user_registered.send(
            sender=self.__class__,
            user=new_user,
            request=self.request
        )
        return new_user