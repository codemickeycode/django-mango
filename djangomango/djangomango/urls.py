from django.contrib import admin
from django.conf.urls import patterns, url, include


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^proposal/', include('proposal.urls')),

    # 3rd-party apps
    url(r'^impersonate/', include('impersonate.urls')),
)
