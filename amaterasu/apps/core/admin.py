from django.contrib import admin
from models import Mailbox, Alias, Domain, PdnsDomains, Records

class MailboxAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'created', 'modified', 'active')
    list_filter = ('created', 'active')
    search_fields = ['username', 'domain']
    
class AliasAdmin(admin.ModelAdmin):
    list_display = ('address', 'goto')
    
class RecordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'content')
    list_filter = ('type',)
    search_fields = ['name', 'type', 'content']
    list_per_page = 25

admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Domain)
admin.site.register(PdnsDomains)
admin.site.register(Records, RecordsAdmin)