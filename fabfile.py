from os import path, pardir
from fabric.api import env, sudo, cd, local, run, settings, prefix, task
from fabric.operations import get, put, open_shell
from fabric.colors import green, red
from pprint import pprint

REMOTE_BASE_PATH = '/var/www/'

env.hosts = ['64.22.109.92']
env.user = 'root'

def copy_files():
    if path.exists('/tmp/amaterasu.zip'):
        local('rm -r /tmp/amaterasu.zip')
        
    local('git archive --format=zip --prefix=amaterasu/ HEAD > /tmp/amaterasu.zip')
    
    put('/tmp/amaterasu.zip', '/tmp/')
    
    with cd(REMOTE_BASE_PATH):
        #run('cp amaterasu/amaterasu/settings.py amaterasu/amaterasu/settings_prod.py')
        run('unzip -o /tmp/amaterasu.zip')
        #run('cp amaterasu/amaterasu/settings_prod.py amaterasu/amaterasu/settings.py')
        
def install_deps():
    with cd(REMOTE_BASE_PATH + 'amaterasu/'):
        with prefix('source ' + REMOTE_BASE_PATH + 'venv/bin/activate'):
            run('pip install -r requirements/requirements.txt')
        
def collectstatic():
    with cd(REMOTE_BASE_PATH + 'amaterasu/'):
        with prefix('source ' + REMOTE_BASE_PATH + 'venv/bin/activate'):
            run('python manage.py collectstatic --noinput')
        
def run_migrations():
    with cd(REMOTE_BASE_PATH + 'amaterasu/'):
        with prefix('source ' + REMOTE_BASE_PATH + 'venv/bin/activate'):
            run('python manage.py migrate')
            
def restart_supervisord():
    sudo('supervisorctl restart amaterasu')
        
def deploy():
    copy_files()
    install_deps()
    #collectstatic()
    run_migrations()
    restart_supervisord()
    print(green('Deployed successfully', bold=True))

