from setuptools import setup

setup(
    name='Resource',
    version='0.13.1',
    long_description=__doc__,
    packages=['backend', 'eieldap'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Fabric>=1.8.1',
        'Flask>=0.9',
        'Flask-Restful>=0.8',
        'Sphinx>=1.2.2',
        'pymongo>=2.7.1',
        'python-ldap>=2.4.10',
        'Pillow>=2.4.0']
    )
