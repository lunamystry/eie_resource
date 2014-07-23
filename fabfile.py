from fabric.api import local, run, env, put, cd, sudo, settings
from fabric.colors import cyan, green
import re
import sys
import fileinput


# the user to use for the remote commands
env.user = 'admin2'
# the servers where the commands are executed
env.hosts = ['resource.eie.wits.ac.za']


def clean():
    print(cyan("cleaning..."))
    local("find . -name '*.pyc' -exec rm -f {} \;", capture=False)
    local("find . -name '__pycache__' -exec rm -rf {} \;", capture=False)
    print(green(u'\u2713'))


def pack():
    # create a new source distribution as tarball
    clean()
    local('python setup.py sdist --formats=gztar', capture=False)


def commit():
    local('git add -A')
    local('git commit')
    local('git push')


def chversion(version):
    def s_and_r(filename, search, replace):
        print(cyan(
            "changing version to version {0} in {1}...".format(version,
                                                               filename)))
        for line in fileinput.input(filename, inplace=True):
            if re.search(search, line):
                line = replace
            sys.stdout.write(line)

    filename = 'frontend/js/services/version.js'
    search = r'service.value'
    replace = "service.value('version', '{}');\n".format(version)
    s_and_r(filename, search, replace)

    filename = 'setup.py'
    search = r'version='
    replace = "    version='{}',\n".format(version)
    s_and_r(filename, search, replace)


def deploy(version):
    chversion(version)
    dist = local('python setup.py --fullname', capture=True).strip()
    pack()
    put('dist/%s.tar.gz' % dist, '/tmp')
    with settings(warn_only=True):
        run('mkdir /tmp/%s' % dist)
        with cd('/tmp/%s' % dist):
            run('tar xzf /tmp/%s.tar.gz' % dist)
            sudo('rm -rf /srv/www/htdocs/vhosts/resource.eie.wits.ac.za')
            sudo('mv /tmp/{0}/{0} /srv/www/htdocs/vhosts/resource.eie.wits.ac.za'.format(dist))
            sudo('chown -R wwwrun:wwwrun /srv/www/htdocs/vhosts/resource.eie.wits.ac.za'.format(dist))
        run('rm -rf /tmp/{0} /tmp/{0}.tar.gz'.format(dist))
        sudo('touch /srv/www/wsgi-scripts/resource.wsgi')
        sudo('rcapache2 restart')
