from django.contrib import admin

from .models import ProposalType, AudienceLevel, Category, Proposal


class ProposalAdmin(admin.ModelAdmin):
    list_display = ['title', 'audience', 'status']


admin.site.register(ProposalType)
admin.site.register(Category)
admin.site.register(AudienceLevel)
admin.site.register(Proposal, ProposalAdmin)
