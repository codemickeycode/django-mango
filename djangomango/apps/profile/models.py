from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from imagekit.models import ImageSpecField
from autoslug import AutoSlugField

from .utils import get_mugshots_path
from ..proposal.models import APPROVED


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    slug = AutoSlugField(
        unique=True,
        always_update=True,
        populate_from=lambda instance: instance.user.get_full_name())
    mugshot = models.ImageField(upload_to=get_mugshots_path)
    mugshot_thumbnail = ImageSpecField(image_field='mugshot',
                                       format='JPEG',
                                       options={'quality': 90})
    bio = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.user.get_full_name()

    def proposals(self):
        """ Return approved proposals. """
        return self.user.proposals.filter(status=APPROVED)

    @models.permalink
    def get_absolute_url(self):
        return ('profile_details', [self.slug])


def create_user_profile(sender, instance, created, **kwargs):
    """ Create a profile for each user created. """
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
