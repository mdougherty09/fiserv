#!/usr/bin/env python

import os
from fabric.api import *

##########################################
## User Decorator                      ###
##########################################

def _setuser(username=None,password=None):
    from functools import wraps

    def decorator_wrap(func):
        @wraps(func)
        def function_wrap(*args,**kwargs):

            # Test to see if command line overrides were used
            if 'un' in env:
                puts("INFO: Using command-line credential override. User=%s" % env.un)
                env.user = env.un
                env.password = env.pw if 'pw' in env else ''
            else:
                # Test to see if dev credentials have been provided in the config file
                if 'devuser' in env:
                    puts("INFO: Using development credentials. User= %s" % env.devuser)
                    env.user = env.devuser
                    env.password = env.devpassword if 'devpassword' in env else ''

                else:
                    # If no username or password were set, use the default username 'tomcat' with a blank password
                    if username is None:
                        env.user = 'tomcat'
                        env.password = ''
                    else:
                        # Use the specified username and password
                        env.user = username
                        env.password = password if password is not None else ''

            # Return the wrapped function with whatever args were passed in
            return func(*args,**kwargs)

        return function_wrap

    return decorator_wrap



env.project_name = '' # Project Name here, eg:  gregaker.net
env.user = '' # user, e.g.:  my_user
env.hosts = [''] # Ip addresses or hostnames
env.path = '' # path, eg:  /var/www/gregaker.net
env.roledefs = {
    'demo-env': [
        'mikesmachine1.sysint.local',
        'mikesmachine2.sysint.local',
        'mikesmachine3.sysint.local',
    ],
    'staging-env': [
        'mikestaging1.sysint.local',
        'mikestaging2.sysint.local',
        'mikestaging3.sysint.local',
    ],
    'production': [
        'machine1.sysint.local',
        'machine2.sysint.local',
        'machine3.sysint.local',
    ],
    }

# A shot at setting up a directory structure
def setup_server():
    """
    Setup Server 
    """
    
    dirs = [
        '/data',
        '%sreleases' % env.path,
        '%sshared' % env.path,
        '%sconfig' % env.path,
        '%spackages' % env.path,
        '%sbackup' % env.path,
    ]
    
    for d in dirs:
        sudo('if [ ! -d "%s" ]; then mkdir -p %s; fi' % (d, d))
    
    sudo('if [ ! -d "%s/env" ]; then cd %s; virtualenv --no-site-packages env; fi' % (env.path, env.path))
    sudo('chown -R %s:%s %s' % (env.user, env.user, env.path))


# Make sure /etc/hosts has the local machine
@parallel
@task
def setup_hosts():
    put(os.path.join(env.SECRETS_PATH, 'configs/hosts'), '/etc/hosts', use_sudo=True)
    sudo('echo "\n\n127.0.0.1   `hostname`" | sudo tee -a /etc/hosts')


# Find and setup logrotate
@_setuser('root')
@task
def setup_logrotate(clear=True):
    if clear:
        run('find /data/sites/*/logs/*.log | xargs tee')
        with settings(warn_only=True):
            sudo('find /var/log/*.log | xargs tee')
    put('config/logrotate.conf', '/etc/logrotate.d/fiserv', use_sudo=True)
    put('config/logrotate.mongo.conf', '/etc/logrotate.d/mongodb', use_sudo=True)
    put('config/logrotate.nginx.conf', '/etc/logrotate.d/nginx', use_sudo=True)
    sudo('chown root.root /etc/logrotate.d/{newsblur,mongodb,nginx}')
    sudo('chmod 644 /etc/logrotate.d/{newsblur,mongodb,nginx}')
    with settings(warn_only=True):
        sudo('chown sclay.sclay /srv/newsblur/logs/*.log')
    sudo('logrotate -f /etc/logrotate.d/fiserv')
    sudo('logrotate -f /etc/logrotate.d/nginx')
    sudo('logrotate -f /etc/logrotate.d/mongodb')


# Change ulimit values
@_setuser('root')
@task
def setup_ulimit():
    # Increase File Descriptor limits.
    run('export FILEMAX=`sysctl -n fs.file-max`', pty=False)
    sudo('mv /etc/security/limits.conf /etc/security/limits.conf.bak', pty=False)
    sudo('touch /etc/security/limits.conf', pty=False)
    run('echo "root soft nofile 100000\n" | sudo tee -a /etc/security/limits.conf', pty=False)
    run('echo "root hard nofile 100000\n" | sudo tee -a /etc/security/limits.conf', pty=False)
    run('echo "* soft nofile 100000\n" | sudo tee -a /etc/security/limits.conf', pty=False)
    run('echo "* hard nofile 100090\n" | sudo tee -a /etc/security/limits.conf', pty=False)
    run('echo "fs.file-max = 100000\n" | sudo tee -a /etc/sysctl.conf', pty=False)
    sudo('sysctl -p')
    sudo('ulimit -n 100000')
    connections.connect(env.host_string)
    
    # run('touch /home/ubuntu/.bash_profile')
    # run('echo "ulimit -n $FILEMAX" >> /home/ubuntu/.bash_profile')

    # Increase Ephemeral Ports.
    # sudo chmod 666 /etc/sysctl.conf
    # echo "net.ipv4.ip_local_port_range = 1024 65535" >> /etc/sysctl.conf
    # sudo chmod 644 /etc/sysctl.conf


# Simple solution for some of our NTP issues
@_setuser('root')
@task
def sync_time():
    with settings(warn_only=True):
        sudo("/etc/init.d/ntp stop")
        sudo("ntpdate pool.ntp.org")
        sudo("/etc/init.d/ntp start")

@_setuser('root')
@task
def setup_time_calibration():
    sudo('apt-get -y install ntp')
    put('config/ntpdate.cron', '%s/' % env.NEWSBLUR_PATH)
    sudo('chown root.root %s/ntpdate.cron' % env.NEWSBLUR_PATH)
    sudo('chmod 755 %s/ntpdate.cron' % env.NEWSBLUR_PATH)
    sudo('mv %s/ntpdate.cron /etc/cron.hourly/ntpdate' % env.NEWSBLUR_PATH)
    with settings(warn_only=True):
        sudo('/etc/cron.hourly/ntpdate')

# Simple start/stop/restart of apps (tomcat)
@_setuser('tomcat')
@task
def start():
    """Start the application servers"""
    sudo("/etc/init.d/tomcat_8080 start")
 
@_setuser('tomcat')
@task
def restart():
    """Restarts your application"""
    sudo("/etc/init.d/tomcat_8080 force-reload")
 
@_setuser('tomcat')
@task
def stop():
    """Stop the application servers"""
    sudo("/etc/init.d/tomcat_8080 stop")

# Run a generic command
@task
def generic_fabric_command(command=''):
    """
    """

    #cmd = raw_input(+command)
    r = command.split(" ")
    cmd = (r[0])
    with cd("/tmp/"):
      open_shell(+cmd)
      pass

# Cleanup Customer Data
@_setuser('dxa')
@task
def cleanup_customer(customer_number=''):
    """
    Will clean up customer data artifacts locally and on the far side
    Args *customer_number 
    """

    local("rm -rf /data/sites/%s" % (customer_number))
    run("rm -rf /data/sites/%s" % (customer_number))
