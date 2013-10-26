from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from autoslug import AutoSlugField
from model_utils import Choices
from model_utils.models import TimeStampedModel

User = get_user_model()


class ProposalType(models.Model):
    """ Talks, Tutorials or Posters """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self)


class Category(models.Model):
    """ Cloud, Education, Databases, etc. """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self)


class AudienceLevel(models.Model):
    """ Novice, Intermediate or Experienced """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self)


class Proposal(TimeStampedModel):

    STATUS = Choices(('pending', 'Pending'),
                     ('approved', 'Approved'),
                     ('declined', 'Declined'))

    speaker = models.ForeignKey(User, related_name='proposals')
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    type = models.ForeignKey(ProposalType, related_name='proposals')
    audience = models.ForeignKey(AudienceLevel, related_name='proposals')
    category = models.ForeignKey(Category, related_name='proposals')
    description = models.TextField()
    abstract = models.TextField()
    duration = models.TimeField()
    status = models.CharField(max_length=10,
                              choices=STATUS,
                              default=STATUS.pending)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return '%s by %s' % (self.title, self.speaker.first_name)

    def __str__(self):
        return unicode(self)

    @models.permalink
    def get_absolute_url(self):
        return ('proposal_details', [self.slug])
