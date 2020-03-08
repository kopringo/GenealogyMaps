from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from .models import ParishUser, Parish


@staff_member_required
def parishes(request):
    data = {}
    return render(request, 'core/_admin/parishes.html', data)


@staff_member_required
def users(request):

    # przelacza aktyacje usera
    switch_ro_access_for_user = request.GET.get('switch_ro_access_for_user', None)
    if switch_ro_access_for_user is not None:
        try:
            user = User.objects.get(pk=int(switch_ro_access_for_user))
            if not user.is_superuser:
                g = Group.objects.get(name='DATA_ACCESS')
                if user.groups.filter(name='DATA_ACCESS').exists():
                    g.user_set.remove(user)
                else:
                    g.user_set.add(user)
        except User.DoesNotExist:
            pass
        return redirect('/a/users')

    # przelacza dostep z pelnego na ograniczony i odwrotnie
    switch_access_for_user = request.GET.get('switch_access_for_user', None)
    if switch_access_for_user is not None:
        try:
            user = User.objects.get(pk=int(switch_access_for_user))
            if not user.is_superuser:
                g = Group.objects.get(name='FULL_DATA_ACCESS')
                if user.groups.filter(name='FULL_DATA_ACCESS').exists():
                    g.user_set.remove(user)
                else:
                    g.user_set.add(user)
        except User.DoesNotExist:
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
        except ParishUser.DoesNotExist:
            return redirect('/a/users?error=parish_user_not_found')
        return redirect('/a/users')

    # parafie zarzadzane przez wiecej osob
    query = 'SELECT * FROM `core_parish` INNER JOIN (SELECT parish_id, count(*) count FROM `core_parishuser` WHERE manager=1 group by parish_id HAVING count>1) c ON id=c.parish_id'
    parishes_with_more_managers = Parish.objects.raw(query)

    # pobieranie userow + sortowanie
    users = User.objects.all()
    sort = request.GET.get('sort', None)
    ord = '-' if request.GET.get('ord', None) == 'desc' else ''
    if sort == 'date':
        users = users.order_by('%s%s' % (ord, 'id'))
    elif sort == 'name':
        users = users.order_by('%s%s' % (ord, 'last_name'), '%s%s' % (ord, 'first_name'))
    elif sort == 'email':
        users = users.order_by('%s%s' % (ord, 'email'))
    else:
        sort = 'date'
        ord = '-'
        users = users.order_by('-id')

    data = {
        'users': users,
        'sort': sort,
        'r_ord': ('desc' if (ord == '') else 'asc'),
        'user_requests': ParishUser.objects.filter(manager_request=True).order_by('-manager_request_date'),
        'parishes_with_more_managers': parishes_with_more_managers
    }

    return render(request, 'core/_admin/users.html', data)

@staff_member_required
def users_user(request, user_id):

    try:
        user = User.objects.get(pk=user_id)
    except:
        return redirect('/a/users')

    remove_id = request.GET.get('remove', None)
    if remove_id is not None:
        try:
            parish = Parish.objects.get(pk=int(remove_id))
            parish_user = ParishUser.objects.get(parish=parish, user=user)
            parish_user.manager = False
            parish_user.save()
        except Exception as e:
            print(e)

        return redirect('/a/users/%d' % user.id)

    if request.POST:
        parishes = request.POST.getlist('parishes')

        for parish_id in parishes:
            try:
                parish = Parish.objects.get(pk=int(parish_id))
                try:
                    parish_user = ParishUser.objects.get(parish=parish, user=user)
                except ParishUser.DoesNotExist:
                    parish_user = ParishUser()

                parish_user.parish = parish
                parish_user.user = user
                parish_user.manager = True
                parish_user.manager_request = False
                parish_user.save()

            except Exception as e:
                print(e)


    data = {
        'user': user,
        'parish_rels': ParishUser.objects.all().filter(user=user, manager=True),
        #'user_requests': ParishUser.objects.filter(manager_request=True).order_by('-manager_request_date')
    }

    return render(request, 'core/_admin/users_user.html', data)