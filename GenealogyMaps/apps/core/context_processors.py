from django.conf import settings as config

def global_settings(request):
    #print config
    return {
        'settings': config,
    }
