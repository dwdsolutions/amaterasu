from django.shortcuts import redirect

def index(request):
    '''
    Redirecciona hacia el administrador
    '''
    return redirect('/admin/', permanent=True)
