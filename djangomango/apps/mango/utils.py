from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site


def moderator_required(user):
    """ Check if user accessing is a moderator. """
    if user.is_authenticated() and user.groups.filter(name='moderator'):
        return True
    return False


def get_site(request=None):
    """ Returns a Site object wether via db or HttpRequest. """
    if Site._meta.installed:
        site = Site.objects.get_current()
    elif request:
        site = RequestSite(request)
    else:
        site = None
    return site
