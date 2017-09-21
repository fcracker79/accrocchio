import os
import sys

from setuptools import setup, find_packages


major, minor1, minor2, release, serial = sys.version_info

readfile_kwargs = {"encoding": "utf-8"} if major >= 3 else {}


def readfile(filename):
    with open(filename, **readfile_kwargs) as fp:
        contents = fp.read()
    return contents


def get_packages(path):
    out = [path]
    for x in find_packages(path):
        out.append('{}/{}'.format(path, x))
    
    return out

packages = get_packages('accrocchio')
setup(name='accrocchio',
      version='0.1.1',
      description='Accrocchio is a library to mark and being notified of smelly code (a.k.a, "accrocchio").',
      url='https://github.com/fcracker79/accrocchio',
      author='fcracker79',
      author_email='fcracker79@gmail.com',
      license='MIT',
      packages=packages,
      install_requires=readfile(os.path.join(os.path.dirname(__file__), "requirements.txt")),
      zip_safe=False,
      test_suite="test",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='accrocchio hinting linting qa'
      )
