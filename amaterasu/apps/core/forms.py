from django import forms
from django.contrib.auth.forms import UserChangeForm
from models import ClientProfile, Domain, Mailbox, Record

class SearchForm(forms.Form):
    """
    Form to search and download a file
    """
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-v', 'placeholder': 'C\'mon, give it a try and enter your link here...'}), label="")
    
class ProfileForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        exclude = ('is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')
        
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        exclude = ('user')
        
class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        exclude = ('client',)
        
class MailboxForm(forms.ModelForm):
    class Meta:
        model = Mailbox
        exclude = ('domain',)
        
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        exclude = ('domain',)
        
class SelectDomainForm(forms.Form):
    domain = forms.ChoiceField(label="Select a Domain", choices=[])
    
    def __init__(self, *args, **kwargs):
        super(SelectDomainForm, self).__init__(*args, **kwargs)
        domains = Domain.objects.filter(active=True)
        domains_choices = []
        for d in domains:
            domains_choices.append((d.id, d.name))
        
        self.fields['domain'].choices = domains_choices
