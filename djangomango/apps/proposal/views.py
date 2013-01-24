from django.contrib import messages
from django.views.generic import CreateView, TemplateView, DetailView, ListView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin

from .forms import SubmitProposalForm
from .models import APPROVED, PENDING, DECLINED, Proposal
from ..mango.utils import moderator_required
from ..mango.templatetags.utils import in_group


class ProposalDetailsView(DetailView):
    template_name = 'proposal/details.html'
    model = Proposal
    context_object_name = 'proposal'

    def get_object(self, queryset=None):
        user = self.request.user
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        try:
            proposal = Proposal.objects.get(slug=slug)

            # only show non-approved proposals to moderators
            if proposal.status != APPROVED and (
                user.is_anonymous() or not in_group(user, 'moderator')):
                raise Http404

            return proposal
        except Proposal.DoesNotExist:
            raise Http404


class SubmitProposalView(LoginRequiredMixin, CreateView):
    form_class = SubmitProposalForm
    template_name = 'proposal/submit.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.speaker = self.request.user
        form.instance.status = PENDING
        form.send_email()
        messages.info(self.request,
            _(u"Thank you, your proposal is now being reviewed."))
        return super(SubmitProposalView, self).form_valid(form)


class ScheduleProposalView(TemplateView):
    template_name = 'proposal/schedule.html'

    @method_decorator(user_passes_test(moderator_required))
    def dispatch(self, *args, **kwargs):
        return super(ScheduleProposalView, self).dispatch(*args, **kwargs)


class ProposalListView(ListView):
    template_name = 'proposal/list.html'
    context_object_name = 'proposal_list'
    queryset = Proposal.objects.all().select_related()

    def get(self, request, *args, **kwargs):
        approve = self.request.GET.get('approve', None)
        decline = self.request.GET.get('decline', None)

        try:
            if approve:
                proposal = Proposal.objects.get(id=int(approve))
                proposal.status = APPROVED
                proposal.save()

            if decline:
                proposal = Proposal.objects.get(id=int(decline))
                proposal.status = DECLINED
                proposal.save()
        except (Proposal.DoesNotExist, ValueError):
            pass
        finally:
            # only redirect if an approve or decline did happened
            if approve or decline:
                return HttpResponseRedirect(reverse('proposal_list'))

        return super(ProposalListView, self).get(request, *args, **kwargs)
