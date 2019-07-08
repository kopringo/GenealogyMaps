from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from .models import ParishUser


@staff_member_required
def users(request):

    # przelacza dostep z pelnego na ograniczony i odwrotnie
    switch_access_for_user = request.GET.get('switch_access_for_user', None)
    if switch_access_for_user is not None:
        print('! ')
        try:
            print('!! ')
            user = User.objects.get(pk=int(switch_access_for_user))
            if not user.is_superuser:
                g = Group.objects.get(name='FULL_DATA_ACCESS')
                if user.groups.filter(name='FULL_DATA_ACCESS').exists():
                    g.user_set.remove(user)
                else:
                    g.user_set.add(user)
        except User.DoesNotExists:
            pass
        return redirect('/a/users')

    access = request.GET.get('access', None)
    if access is not None:
        user = request.GET.get('user', None)
        parish = request.GET.get('parish', None)
        try:
            parish_user = ParishUser.objects.get(parish=parish, user=user)
            parish_user.manager = True
            parish_user.manager_request = False
            parish_user.manager_request_date = None
            parish_user.save()
        except ParishUser.DoesNotExists:
            return redirect('/a/users?error=parish_user_not_found')
        return redirect('/a/users')

    data = {
        'users': User.objects.all().order_by('-id'),
        'user_requests': ParishUser.objects.filter(manager_request=True).order_by('-manager_request_date')
    }

    return render(request, 'core/_admin/users.html', data)
