# Fiserv
Getting code to Fiserv -- Mike Dougherty
----------------------------------------

Included:
--------------
 - DeployKeys.py (simple python to deploy ssh keys)
--------------

 - Ansible (ansible playbooks and roles to get things started)
   -- There are some downloaded roles in here
      -> mongodb (will go soup to nuts for setting up a cluster, README included)
      -> jenkins (Out of the box install of Jenkins CI)
      -> tomcat (simple tomcat deployment)

   -- Thoughts on Ansible setup and advise.

         How the structure is layed down in the beginning is crucial.  Think about your environment as a whole and have it controled by a single YAML file.  We need to make sure that there are no one-off changes to machines.  If something needs to be fixed in a hurry, I get it.  Change the file and immediately make sure that change is reflected in code or it will be overwritten eventually and nobody will know why.

         Learn to standardize a "type of machine" and group your roles for that specific type accordingly.  All servers should have the same base packages, but the machine types will tell you what add-on services and packages are needed for that class of machine.

         Keep your playbooks small.  Don't try to do too much in one playbook, you will find ways and needs to re-use bits of code all of the time.  Also, it is much easier to write smaller blocks of code for people who may not be experts in the subject.  You will also find debug to be simpler when dealing with small chunks instead of a huge monolythic peice of code.

         Try to keep with a directory structure like the following:
              inventories/
                 production/
                    hosts               # inventory file for production servers
                    group_vars/
                       group1           # here we assign variables to particular groups
                       group2           # ""
                    host_vars/
                       hostname1        # if systems need specific variables, put them here
                       hostname2        # ""

                 staging/
                    hosts               # inventory file for staging environment
                    group_vars/
                       group1           # here we assign variables to particular groups
                       group2           # ""
                    host_vars/
                       stagehost1       # if systems need specific variables, put them here
                       stagehost2       # ""

              library/
              filter_plugins/

              site.yml                  # Master playbook will assign machine groups to tasks

              roles/
                  base/
                    files/              # Files to be copied to target machine
                    tasks/              # main.yml and sub tasks
                    templates/          # j2 template files
                  webtier/
                    files/
                    tasks/
                    templates/
                  monitoring/
                    files/
                    tasks/
                    templates/
                  mongodb/
                    files/
                    tasks/
                    templates/
                  mysql/
                    files/
                    tasks/
                    templates/
                  tomcat/
                    files/
                    tasks/
                    templates/
                  java/
                    files/
                    tasks/
                    templates/
                  ntp/
                    files/
                    tasks/
                    templates/
                  OneOffs/

######  Note ######
   Please see my example site.yml and host file

--------------

 - Vagrant (Vagrant file example for VirtualBox and a provider section for VCenter)

     Start using this in tandem with your ansible environment.  It will give you a way to test your code as it is being deployed.  Take a look at the example and check out the provisioner sections.  You will see that I am not just using Vagrant to launch machines, but I am also using ansible to provision the machines with patches/apps/etc...

--------------

 - Fabric

     Some of you may have heard me talk about fabric.  It is a good general purpose sysAdmin tool framwork.  Written in a very simple python'ish way.  You can use it to give people a common way to do some day to day tasks.  I am including a fabfile that I had started working on for Fiserv.  
     To install fabric, just run 'pip install fabric'.  There is also a plugin for the f5 which can be very useful when working with the API.  To install that run 'pip install pycontrol'.
     For more information on this tool, please visit http://www.fabfile.org
