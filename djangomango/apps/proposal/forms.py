import logging
import smtplib

from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from .models import Proposal
from ..mango.utils import get_site


logger = logging.getLogger('generic')


class SubmitProposalForm(forms.ModelForm):
    duration = forms.CharField(widget=forms.TimeInput(
        attrs={'placeholder': '00:00'}))

    class Meta:
        model = Proposal
        fields = ('title', 'type', 'audience', 'category', 'duration',
                  'description', 'abstract')

    def send_email(self):
        """ Send email to notify moderators about the new submission. """
        moderator_emails = User.objects.filter(groups__name='moderator',
            is_active=True).values_list('email', flat=True)

        context = {'proposal_title': self.instance.title,
                   'submitted_by': self.instance.speaker.get_full_name(),
                   'site_name': get_site().name}
        subject = render_to_string('proposal/email/submission_subject.html').strip()
        message = render_to_string('proposal/email/submission_body.html', context)

        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      moderator_emails)
        except smtplib.SMTPException as e:
            logger.error('Unable to send email: %s' % str(e))
