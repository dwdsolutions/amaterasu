import os
from fabric.api import *
from fabric.colors import green, red
from pprint import pprint

REMOTE_BASE_PATH = '/var/www/'

env.hosts = ['64.22.109.92']
env.user = 'root'

def copy_files():
    if os.path.exists('/tmp/amaterasu.zip'):
        local('rm -r /tmp/amaterasu.zip')
        
    local('git archive --format=zip --prefix=amaterasu/ HEAD > /tmp/amaterasu.zip')
    
    put('/tmp/amaterasu.zip', '/tmp/')
    
    with cd(REMOTE_BASE_PATH):
        run('unzip -o -f /tmp/amaterasu.zip')
        
def install_deps():
    with cd(REMOTE_BASE_PATH):
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
        
def deploy():
    copy_files()
    collectstatic()
    print(green('Deployed successfully', bold=True))

