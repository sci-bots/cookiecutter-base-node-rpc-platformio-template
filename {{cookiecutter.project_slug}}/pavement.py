from collections import OrderedDict
from importlib import import_module
import os
import sys

from paver.easy import task, needs, path, sh, options
try:
    from base_node_rpc.pavement_base import *
except ImportError:
    pass

# add the current directory as the first listing on the python path
# so that we import the correct version.py
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import version
# Add package directory to Python path. This enables the use of
# `{{cookiecutter.project_module_name}}` functions for discovering, e.g., the
# path to the Arduino firmware sketch source files.
sys.path.append(path('.').abspath())

# Import project module.
rpc_module = import_module('{{cookiecutter.project_module_name}}')
VERSION = version.getVersion()
PROPERTIES = OrderedDict([('name', '{{cookiecutter.project_slug}}'),
                          ('package_name', '{{cookiecutter.project_slug}}'),
                          ('manufacturer', '{{cookiecutter.hardware_manufacturer}}'),
                          ('software_version', VERSION),
                          ('url', 'https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}')])

# XXX Properties used to generate Arduino library properties file.
LIB_PROPERTIES = PROPERTIES.copy()
LIB_PROPERTIES.update(OrderedDict([('author', '{{cookiecutter.full_name}}'),
                                   ('author_email', '{{cookiecutter.email}}'),
                                   ('short_description', '{{cookiecutter.project_short_description}}'),
                                   ('version', VERSION),
                                   ('long_description', ''),
                                   ('category', '{{cookiecutter.arduino_category}}'),
                                   ('architectures', '{{cookiecutter.arduino_architectures}}')]))

options(
    rpc_module=rpc_module,
    PROPERTIES=PROPERTIES,
    LIB_PROPERTIES=LIB_PROPERTIES,
    base_classes=['BaseNodeSerialHandler',
                  'BaseNodeEeprom',
                  'BaseNodeI2c',
                  'BaseNodeI2cHandler<Handler>',
                  'BaseNodeConfig<ConfigMessage, Address>',
                  'BaseNodeState<StateMessage>'],
    rpc_classes=['{{cookiecutter.project_module_name}}::Node'],
    setup=dict(name=PROPERTIES['name'],
               version=VERSION,
               description='{{cookiecutter.project_short_description}}',
               author='{{cookiecutter.full_name}}',
               author_email='{{cookiecutter.email}}',
               url=PROPERTIES['url'],
               license='BSD',
               install_requires=['wheeler.base_node_rpc>=0.23'],
               include_package_data=True,
               packages=['{{cookiecutter.project_module_name}}']))


@task
@needs('base_node_rpc.pavement_base.generate_all_code')
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
