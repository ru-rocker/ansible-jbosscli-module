# ansible-jbosscli-module
Ansible module for jboss-cli command. All these modules are tested using wildfly 10.0.

# Modules
### Server group module     
This module is intended to do operation related with server-group, and only works for domain mode only. 
There are several states for this module:
* present: server group is created
* absent: server group is deleted
* start: start all server in the server group
* stop: stop all server in the server group

### Server module
This module is intended to do operation with server within server group, and only works for domain mode only. 
There are several states for this module:
* present: server is created and started
* absent: server is deleted
* start: start the server
* stop: stop the server
     
### JVM module
This module is intended to setting jvm for each server, and only works for domain mode only.
There are two states for this module:
* present: jvm paramaters are set to target server
* absent: jvm parameters are removed from target server

### Deployment module
This module is intended for deploy or undeploy ear/war and can be used for standalone/domain mode.
There are two states for this module:
* present: deploy ear/war
* absent: undeploy ear/war

# Play
There are 4 play files:
* play.yml: as a sample to create from server group to deploy war
* play_absent.yml: as a sample to undeploy war until deleting server group
* play_server_start_stop.yml: a sample file to start/stop server
* play_servergroup_start_stop.yml: a sample file to start/stop all server in a server group

How to run:

    
    ansible-playbook play.yml

# TODO
* Several function like creating data-source, queue or topic still has not been covered
* Documentation in .py files
* Better error handling?
