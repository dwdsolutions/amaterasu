from django.contrib import admin
from models import Mailbox, Alias, Domain, PdnsDomains, Records, Language, Plan, ClientProfile

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
    
class PlanAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Nombre Plan', {'fields': ['nombre']}),
        ('Espacios', {'fields': ['espacio', 'transferencia', 'cuentas_correo', 'subdominios', 'cuentas_ftp', 'db_mysql', 'db_postgres']}),
        ('Lenguajes', {'fields': ['lenguajes']}),
        ('Precio', {'fields': ['precio']}),
    ]
    #inlines = [AdicionalInline]
    list_display = ('nombre', 'espacio', 'transferencia', 'db_mysql', 'db_postgres', 'precio')

    
class ClientProfileAdmin(admin.ModelAdmin):
    list_displat = ('get_full_name', 'phone', 'email')

admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Domain)
admin.site.register(PdnsDomains)
admin.site.register(Records, RecordsAdmin)
admin.site.register(Language)
admin.site.register(Plan, PlanAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)

