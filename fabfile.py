from fabric.api import *

# the user to use for the remote commands
env.user = 'admin2'
# the servers where the commands are executed
env.hosts = ['babbage.ug.eie.wits.ac.za']

def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/resource.tar.gz')
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir /tmp/resource')
    with cd('/tmp/resource'):
        run('tar xzf /tmp/resource.tar.gz')
        # now setup the package with our virtual environment's
        # python interpreter
        run('/srv/htdocs/www/resource/env/bin/python setup.py install')
    # now that all is set up, delete the folder again
    run('rm -rf /tmp/resource /tmp/resource.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run('touch /var/www/resource.wsgi')

def set-env():
    "Intended to add convinience aliases to the bashrc file."
    pass
