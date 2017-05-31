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

 - vagrant (Vagrant file example for VirtualBox and a provider section for VCenter)
