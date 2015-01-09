#! /bin/bash 

# Select current version of virtualenv:
VERSION=12.0.5
# Name your first "bootstrap" environment:
INITIAL_ENV=env0
# Options for your first environment:
ENV_OPTS='--no-site-packages --distribute'
# Set to whatever python interpreter you want for your first environment:
PYTHON=$(which python)
URL_BASE=http://pypi.python.org/packages/source/v/virtualenv
VIRTUALENV_DIR=$HOME/.bin/virtualenvironments

# --- Real work starts here ---

cur_dir=pwd

if [ ! -d $VIRTUALENV_DIR ]; then
    mkdir -p $VIRTUALENV_DIR
fi
cd $VIRTUALENV_DIR

wget $URL_BASE/virtualenv-$VERSION.tar.gz
tar xzf virtualenv-$VERSION.tar.gz
# Create the first "bootstrap" environment.
$PYTHON virtualenv-$VERSION/virtualenv.py $ENV_OPTS $INITIAL_ENV
# Install virtualenv into the environment.
$INITIAL_ENV/bin/pip install virtualenv-$VERSION.tar.gz
# Don't need this anymore.
rm -rf virtualenv-$VERSION
rm -rf virtualenv-$VERSION.tar.gz

#activate the initial env
. $VIRTUALENV_DIR/$INITIAL_ENV/bin/activate

cd $curr_dir
