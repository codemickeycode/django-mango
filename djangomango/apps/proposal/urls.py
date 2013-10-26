from django.conf.urls import patterns, url

from .views import (ProposalListView,
                    SubmitProposalView,
                    ProposalDetailsView)


urlpatterns = patterns('',
    url(
        r'^$',
        ProposalListView.as_view(),
        name='proposal_list'
    ),
    url(
        r'^submit/$',
        SubmitProposalView.as_view(),
        name='submit_proposal'
    ),
    url(
        r'^(?P<slug>[-\w]+)/$',
        ProposalDetailsView.as_view(),
        name='proposal_details'
    ),
)
