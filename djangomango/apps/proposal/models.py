import logging
import smtplib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from autoslug import AutoSlugField

from ..mango.models import BaseModel
from ..mango.utils import get_site


logger = logging.getLogger('generic')


PENDING = 'pending'
APPROVED = 'approved'
DECLINED = 'declined'

PROPOSAL_STATUS = (
    (PENDING, _(u'Pending')),
    (APPROVED, _(u'Approved')),
    (DECLINED, _(u'Declined'))
)


class ProposalType(models.Model):
    """ Talks, Tutorials or Posters """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """ Cloud, Education, Databases, etc. """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return self.name


class AudienceLevel(models.Model):
    """ Novice, Intermediate or Experienced """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Proposal(BaseModel):
    speaker = models.ForeignKey(User, related_name='proposals')
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    type = models.ForeignKey(ProposalType)
    audience = models.ForeignKey(AudienceLevel)
    category = models.ForeignKey(Category)
    description = models.TextField()
    abstract = models.TextField()
    duration = models.TimeField()
    status = models.CharField(max_length=10, choices=PROPOSAL_STATUS,
                              default='pending')

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('proposal_details', [self.slug])


def send_email_notification(sender, instance, **kwargs):
    """ Send email notification when a proposal has been approved/declined. """

    # only continue if this proposal has been previously saved,
    # to avoid sending email for newly created proposal.
    if not instance.id:
        return

    site = get_site()
    old_proposal = Proposal.objects.get(id=instance.id)
    protocol = 'http' if not settings.current_request.is_secure() else 'https'
    context = {'proposal_title': instance.title,
               'proposal_url': instance.get_absolute_url(),
               'domain': site.domain,
               'site_name': site.name,
               'protocol': protocol}
    subject = render_to_string('proposal/email/status_subject.html').strip()

    if instance.status == APPROVED and old_proposal.status != APPROVED:
        message_tpl = 'proposal/email/status_approved_body.html'
    elif instance.status == DECLINED and old_proposal.status != DECLINED:
        message_tpl = 'proposal/email/status_declined_body.html'
    else:
        # No change
        return

    try:
        message = render_to_string(message_tpl, context)
        msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,
                           [instance.speaker.email])
        msg.content_subtype = "html"
        msg.send()
    except smtplib.SMTPException as e:
        logger.error('Unable to send email: %s' % str(e))


pre_save.connect(send_email_notification, sender=Proposal)
