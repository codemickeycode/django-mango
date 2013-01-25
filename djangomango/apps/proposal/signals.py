import logging
import smtplib

from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.dispatch import receiver

from .models import Proposal, APPROVED, DECLINED
from ..mango.utils import get_site


logger = logging.getLogger('generic')


@receiver(post_save, sender=Proposal)
def send_email_notification(sender, instance, created, **kwargs):
    """ Send email notification when a proposal has been approved/declined. """

    # only continue if this proposal has been previously saved,
    # to avoid sending email for newly created proposal.
    if created:
        return

    site = get_site()
    proposal_url = (settings.current_request
                    .build_absolute_uri(instance.get_absolute_url()))
    context = {'proposal_title': instance.title,
               'proposal_url': proposal_url,
               'site_name': site.name}
    subject = render_to_string('proposal/email/status_subject.html').strip()

    if instance.status == APPROVED:
        message_tpl = 'proposal/email/status_approved_body.html'
    elif instance.status == DECLINED:
        message_tpl = 'proposal/email/status_declined_body.html'
    else:
        # No change
        return

    try:
        message = render_to_string(message_tpl, context).strip()
        msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,
                           [instance.speaker.email])
        msg.content_subtype = 'html'
        msg.send()
    except smtplib.SMTPException as e:
        logger.error('Unable to send email: %s' % str(e))
