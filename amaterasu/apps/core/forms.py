from django import forms
from django.contrib.auth.forms import UserChangeForm
from models import ClientProfile

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
