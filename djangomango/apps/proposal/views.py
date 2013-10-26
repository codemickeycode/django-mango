from django.contrib import messages
from django.views.generic import CreateView, TemplateView, DetailView, ListView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.core.urlresolvers import reverse

from .forms import SubmitProposalForm
from .models import Proposal
from libs.utils import moderator_required


class ProposalListView(ListView):
    model = Proposal
    template_name = 'proposal/list.html'


class SubmitProposalView(CreateView):
    form_class = SubmitProposalForm
    template_name = 'proposal/submit.html'

    def get_success_url(self):
        return reverse('submit_proposal')

    def get_context_data(self, *args, **kwargs):
        return super(SubmitProposalView, self).get_context_data(*args, **kwargs)

    def form_valid(self, form):
        form.instance.speaker = self.request.user
        form.instance.status = Proposal.STATUS.pending
        messages.success(self.request, _(u"Thank you, your proposal is now being reviewed."))
        return super(SubmitProposalView, self).form_valid(form)


class ProposalDetailsView(DetailView):
    template_name = 'proposal/details.html'
    model = Proposal
    context_object_name = 'proposal'

    # def get_object(self, queryset=None):
    #     slug = self.kwargs.get(self.slug_url_kwarg, None)
    #     try:
    #         return Proposal.objects.get(slug=slug, status=Proposal.STATUS.approved)
    #     except Proposal.DoesNotExist:
    #         raise Http404
