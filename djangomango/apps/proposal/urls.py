from django.conf.urls.defaults import patterns, url

from .views import (SubmitProposalView, ScheduleProposalView,
                    ProposalDetailsView, ProposalListView)


urlpatterns = patterns('',
    url(
        r'^list/$',
        ProposalListView.as_view(),
        name='proposal_list'
    ),
    url(
        r'^submit/$',
        SubmitProposalView.as_view(),
        name='submit_proposal'
    ),
    url(
        r'^schedule/$',
        ScheduleProposalView.as_view(),
        name='schedule_proposal'
    ),
    url(
        r'^(?P<slug>[-\w]+)/$',
        ProposalDetailsView.as_view(),
        name='proposal_details'
    ),
)
