from django.conf import settings as config

def global_settings(request):
    #print config
    return {
        'settings': config,
    }


def show_toolbar(request):
    """
    Default function to determine whether to show the toolbar on a given page.
    """
    return config.DEBUG or request.user.is_superuser
