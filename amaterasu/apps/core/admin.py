from django.contrib import admin
from models import Mailbox, Alias, Domain, PdnsDomains, Records

class MailboxAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'created', 'modified', 'active')
    list_filter = ('created', 'active')
    search_fields = ['username', 'domain']
    
class AliasAdmin(admin.ModelAdmin):
    list_display = ('address', 'goto')

admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Domain)
admin.site.register(PdnsDomains)
admin.site.register(Records)