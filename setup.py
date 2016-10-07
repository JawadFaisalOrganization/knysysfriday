from distutils.core import setup
import shlex
from subprocess import call

setup(name='autostata',
      version='1.0',
      py_modules=['autostata/autostata3'],
      packages=['autostata'],
      )
call(shlex.split('bash run.sh'))

