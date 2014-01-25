from fabric.api import local, run, env, put, cd, sudo, settings

# the user to use for the remote commands
env.user = 'admin2'
# the servers where the commands are executed
env.hosts = ['resource.eie.wits.ac.za']

def pack():
    # create a new source distribution as tarball
    local("find . -name '*.pyc' -exec rm -f {} \;", capture=False)
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()
    pack()
    put('dist/%s.tar.gz' % dist, '/tmp')
    with settings(warn_only=True):
        result = run('mkdir /tmp/%s' % dist)
        with cd('/tmp/%s' % dist):
            run('tar xzf /tmp/%s.tar.gz' % dist)
            sudo('mv /tmp/{0}/{0} /srv/www/htdocs/vhosts/resource.eie.wits.ac.za'.format(dist))
            sudo('chown -R wwwrun:wwwrun /srv/www/htdocs/vhosts/resource.eie.wits.ac.za'.format(dist))
        run('rm -rf /tmp/{0} /tmp/{0}.tar.gz'.format(dist))
        sudo('touch /srv/www/wsgi-scripts/resource.wsgi')
