from os import environ
from dotenv import load_dotenv
from fabric.tasks import task


load_dotenv()
PYTHON = environ.get('SERVER_PYTHON_PATH')
ACTIVATE_VENV = environ.get('ACTIVATE_VENV', 'source .venv/bin/activate')
USERNAME = environ.get('USERNAME')
PROJECTS_PATH = environ.get('PROJECTS_PATH')
PROJECT_NAME = environ.get('PROJECT_NAME')
GIT_REPOSITORY = environ.get('GIT_REPOSITORY')


@task
def install(c):
    """
    Install project on remote server
    fab install --hosts=<ip> (IP or record from .ssh/config)
    """
    c.run(f'mkdir {PROJECTS_PATH}/{PROJECT_NAME}')
    with c.cd(f'{PROJECTS_PATH}/{PROJECT_NAME}'):
        c.run(f'git clone {GIT_REPOSITORY} .')
        c.run(f'{PYTHON} -m venv .venv')
        c.run(f'{ACTIVATE_VENV} && pip install --upgrade pip')
        c.run(f'{ACTIVATE_VENV} && pip install -r requirements.txt')
        c.run('cp .env-dist .env')


@task
def upload(c, local, remote):
    """
    Upload file
    fab upload --local=</path/to/local/file> --remote=<relative/path/to/file> --hosts=<ip>
    """
    c.put(local, f'{PROJECTS_PATH}/{PROJECT_NAME}/{remote}')


@task
def download(c, remote, local):
    """
    Download file
    fab download --remote=<relative/path/to/file> --local=</path/to/local/file> --hosts=<ip>
    """
    c.get(f'{PROJECTS_PATH}/{PROJECT_NAME}/{remote}', local)


@task
def deploy(c, branch='master', deps=False):
    """
    Deploy updates to server
    fab deploy --branch=<name> --deps --hosts=<ip>
    """
    with c.cd(f'{PROJECTS_PATH}/{PROJECT_NAME}'):
        print('> Updating code')
        c.run(f'git fetch origin && git checkout {branch} && git pull origin {branch}')
        if deps:
            print('> Installing dependencies')
            c.run(f'{ACTIVATE_VENV} && pip install -r requirements.txt')


@task
def service(c, name="nginx", action="restart"):
    """
    System service status|start|stop|restart
    fab service --name=<service_name> --action=<action> --hosts=<ip>
    """
    print(f'> {action} {name}')
    c.run(f'sudo service {name} {action}')


@task
def status(c, project):
    """
    Get project services status
    fab status --project=<name> --hosts=<ip>
    """
    c.run(f'systemctl | grep {project}')


@task
def logs(c, service, follow=False):
    """
    Get services logs
    fab logs --service=<name> --follow --hosts=<ip>
    """
    params = '-f' if follow else '-n 100'
    c.run(f'sudo journalctl -u {service} {params}')
