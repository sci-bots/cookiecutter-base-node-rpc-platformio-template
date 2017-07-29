import os
import sys

from paver.easy import task, needs, path, sh
from paver.setuputils import setup

# add the current directory as the first listing on the python path
# so that we import the correct version.py
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import version
# Add package directory to Python path. This enables the use of
# `{{cookiecutter.project_module_name}}` functions for discovering, e.g., the path to the Arduino
# firmware sketch source files.
sys.path.append(path('.').abspath())

setup(name='{{cookiecutter.project_slug}}',
      version=version.getVersion(),
      description='{{cookiecutter.project_short_description}}',
      author='{{cookiecutter.full_name}}',
      author_email='{{cookiecutter.email}}',
      url='https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}',
      license='MIT',
      packages=['{{cookiecutter.project_module_name}}', '{{cookiecutter.project_module_name}}.bin'])


@task
def build_firmware():
    sh('pio run')


@task
def upload():
    sh('pio run --target upload --target nobuild')


@task
@needs('generate_setup', 'minilib', 'build_firmware',
       'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
