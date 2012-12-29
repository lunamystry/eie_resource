from setuptools import setup

setup(
    name='Resource',
    version='0.1',
    long_description=__doc__,
    packages=['resource'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.9',
        'Jinja2>=2.6',
        'Hamlish-Jinja>=0.2.0',
        'Flask-KVSession>=0.3.2',
        'Flask-WTF>=0.8',
        'WTForms>=1.0.2',
        'Werkzeug>=0.8.3',
        'python-ldap>=2.4.10',
        'Flask-Login>=0.1.3',
        'SQLAlchemy>=0.6',
        'Fabric>=1.5.1']
    )
