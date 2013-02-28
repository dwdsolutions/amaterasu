from models import Usuario, Group, Quota_Limit
from django.contrib import admin

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('userid', 'homedir', 'accessed', 'modified')
    search_fields = ['userid']

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Group)
admin.site.register(Quota_Limit)