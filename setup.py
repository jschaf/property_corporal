try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt")
config = {
    'description': 'My Project',
    'author': 'Joe Schafer',
    'url': 'https://github.com/jschaf/property_corporal',
    'download_url': 'https://github.com/jschaf/property_corporal',
    'author_email': 'joe@jschaf.com',
    'version': '0.01',
    'install_requires': [str(ir.req) for ir in install_reqs],
    'packages': ['property_corporal'],
    'scripts': [],
    'name': 'property_corporal'
}

setup(**config)
