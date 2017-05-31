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

--------------

- TLS/SSL termination on the F5

     Very detailed instructions can be found at https://www.lullabot.com/articles/setting-up-ssl-offloading-termination-on-an-f5-bigip-load-balancer

--------------


 - Random thoughts and strategy (Take it for what it's worth)

     I can not stress enough the importance of limiting the one-off fixes.  Infrastructure As Code (IAAC) is a dicipline not a guideline.  Everyone has to be onboard or all will be lost.  Take some time and think about solutions in place.  Find the low hanging fruit and get some quick wins.  Most of all, start thinking like developers.  All to often, we find ourselves putting things into production with out the necessary automation/documentation around it.  We can not get into another situation where we have 1 expert that is reliant upon.  If something needs to get into production, it needs to be at very least repeatable.

     Develop tools for common issues.  Have them organized and checked into some kind of version control.  If this is done, bringing new people on becomes less of a hassle.  They can have the tools in front of them when they need it prior to being completely comfortable in the environment.

     Flatten out the network.  The 1990's pod structure is over and no longer needed.  Try to simplify things with an approach similar to a cloud.  Webtier > appTier > dbTier > ancilaryAppTier.  With this approach, you will find management of the application so much easier.

     Distribute the load.  The F5's you have there are some pretty amazing tools.  From what I understand, the application is almost entirely stateless.  Build it all behind VIPS and pools and your customers will appreciate the performance increase.

     Build automation around a minimal install.  I have started this process in the ansible checkins.  Have your base vmware image be a minimal install and have the bootstrap process be automated.  Nobody should need to follow a checklist to stand up a machine.  If we can take time to write somethin in Excel, we should have had enough time to port that into something a little less manual.  Again, this should be done with very small playbooks or cookbooks or whatever you decide on.

     Get in front of Dev.  Remember, if you don't get involved in the conversations early, then you should not expect to have a say in the outcome.  They are constantly working months ahead and may not be completely informed in all of the tech that is in place currently.  This will always be your opportunity to have a voice in what the product will become.

     Rotate your on-call duties.  I always found it most helpful when we used the following:

############

       Point person on-call for 1 week.
         The person who is supposed to go on-call next is the escalation point.  Third is Clint.
       Person who was on-call the prior week has actionable duties.  (tickets that come in, elevations to staging, etc)
     So the rotation from your standpoint is ( Escalation Point => On-Call => Actionable Duties => Profit )
     This way, not everyone's phone rings all of the time and you get to learn a great deal about the environment for the week you are the "Action Point"

############

     Find a way to collapse similar technologies.  The Wild West show should be coming to an end.  You don't need 4 different types of FTP server for example.  Find a way to limit the tech everyone needs to be an expert on daily and things will stablize and people can work on the cooler projects that they want. 

     Get Gentoo the hell out of there :-)  Since everything has been custom compiled, a lift and replace effort should be fairly minimal.  That being said, my next pice of advise is to use more upstream technology.  Stop custom compiling and use the rpms that you are given.  If you can use the upstream rpms, build one yourself.  You are going to find that you can get your answers and fixes so much faster if you are not the oddball.

     Teach the project managers how they need to communicate.  Looking at some of the tickets that come in, I often felt like I needed a Rosetta Stone to make any sense of it.  Work with them on thier workflows and how you need to see the information as it comes in.  Believe me, this is a win-win for everyone involved.  You won't have to try to guess what the heck everyone is talking about, and they will get more tickets done because of it.  This is one that should be considered not only important, but very accomplishable.

     Build more environments.  This one is obvious, the SDLC (Standard Development Life Cycle) is a standard for a very good reason.  It let's not only dev develop in a production like environment, but dev-ops as well.  Test your code on something as close to production as possible and 75% of your problems disappear.


--------------

 - Final thoughts

     I am going to leave this repo up and I will contribute where I can.  Most of you have my personal number if you need some quick advise or guidance and I will be more than happy to help.  I want to let everyone know that if this weren't such a tremendous opportunity for myself and my family, I wouldn't have ever considered leaving.
