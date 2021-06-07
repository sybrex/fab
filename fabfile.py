from os import environ
from dotenv import load_dotenv
from fabric.tasks import task


load_dotenv()
PYTHON = environ.get('SERVER_PYTHON_PATH', '/usr/local/bin/python3.8')
ACTIVATE_VENV = environ.get('ACTIVATE_VENV', 'source .venv/bin/activate')
USERNAME = environ.get('USERNAME', 'deployer')
PROJECTS_PATH = environ.get('PROJECTS_PATH', '/var/www/vhosts')
PROJECT_NAME = environ.get('PROJECT_NAME', 'fab')
GIT_REPOSITORY = environ.get('GIT_REPOSITORY')


@task
def install(c, project):
    """
    Install project
    fab install --project=<name> --hosts=<ip>
    """
    c.run(f'mkdir {PROJECTS_PATH}/{project}')
    with c.cd(f'{PROJECTS_PATH}/{project}'):
        c.run(f'git clone {GIT_REPOSITORY} .')
        c.run(f'{PYTHON} -m venv .venv')
        c.run(f'{ACTIVATE_VENV} && pip install --upgrade pip')
        c.run(f'{ACTIVATE_VENV} && pip install -r requirements.txt')
        c.run('cp .env-dist .env')


@task
def upload(c, project, local, remote):
    """
    Upload file
    fab upload --project=<name> --local=</path/to/local/file> --remote=<relative/path/to/file> --hosts=<ip>
    """
    c.put(local, f'{PROJECTS_PATH}/{project}/{remote}')


@task
def download(c, project, remote, local):
    """
    Download file
    fab download --project=<name> --remote=<relative/path/to/file> --local=</path/to/local/file> --hosts=<ip>
    """
    c.get(f'{PROJECTS_PATH}/{project}/{remote}', local)


@task
def deploy(c, project, branch='master', deps=False):
    """
    Deploy updates to server
    fab deploy --project=<name> --branch=<name> --deps --hosts=<ip>
    """
    with c.cd(f'{PROJECTS_PATH}/{project}'):
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
