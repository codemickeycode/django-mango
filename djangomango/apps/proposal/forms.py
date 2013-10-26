from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Column, Submit, Field

from .models import Proposal


class SubmitProposalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('title',
                       'type',
                       'audience',
                       'category',
                       Field('duration', placeholder='00:00'),
                       css_class='large-6'),
                Column('abstract',
                       'description',
                       css_class='large-6')),
            Row(Submit('save', _('Save'), css_class='radius'),
                css_class='form-actions'))
        super(SubmitProposalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Proposal
        fields = ('title', 'type', 'audience', 'category', 'duration',
                  'description', 'abstract')
