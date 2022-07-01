from django.conf import settings


def app_version(request):
    return {'APP_VERSION_NUMBER': settings.APP_VERSION_NUMBER}


def whats_new_url(request):
    return {'WHATS_NEW_URL': settings.WHATS_NEW_URL}