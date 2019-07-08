from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



@login_required
def users(request):

    data = {
        'users': User.objects.all().order_by('-id')
    }


    return render(request, 'core/_admin/users.html', data)
