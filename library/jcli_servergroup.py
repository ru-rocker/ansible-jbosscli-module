#!/usr/bin/python

from ansible.module_utils.basic import *
import subprocess
import json

def isServerGroupAlreadyCreated(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    cli = "/server-group=%s:query" % (data['server_group_name'])
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    p = subprocess.Popen(["sh", cmd, "-c", cli, controller], stdout=subprocess.PIPE)
    result , err = p.communicate()

    print(err)

    if "WFLYCTL0216" in result:
        return False
    else:
        return True

def server_group_present(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    exists = isServerGroupAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}

    if not exists:
        cli1 = "/server-group=%s:add(profile=%s, socket-binding-group=%s)" % (data['server_group_name'],data['server_group_profile'],data['socket_binding_group'])
        controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
        p = subprocess.Popen(["sh", cmd, "-c", cli1, controller], stdout=subprocess.PIPE)
        result,err = p.communicate()
        meta = {"status": "OK", "response": result}
    else:
        hasChanged = False
        resp = "Server group %s already created" % (data['server_group_name'])
        meta = {"status" : "OK", "response" : resp}

    return isError, hasChanged, meta

def server_group_absent(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    exists = isServerGroupAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}

    if not exists:
        hasChanged = False
        resp = "Server group %s does not exist" % (data['server_group_name'])
        meta = {"status" : "OK", "response" : resp}
    else:
        cli1 = "/server-group=%s:remove" % (data['server_group_name'])
        controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
        p = subprocess.Popen(["sh", cmd, "-c", cli1, controller], stdout=subprocess.PIPE)
        result,err = p.communicate()
        meta = {"status": "OK", "response": result}

    return isError, hasChanged, meta

def server_group_start(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    exists = isServerGroupAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}

    if exists:
        cli1 = "/server-group=%s:start-servers" % (data['server_group_name'])
        p = subprocess.Popen(["sh", cmd, "-c", cli1, controller], stdout=subprocess.PIPE)
        result,err = p.communicate()
        meta = {"status": "OK", "response": result}
    else:
        hasChanged = False
        resp = "Server group %s does not exist" % (data['server_group_name'])
        meta = {"status" : "OK", "response" : resp}

    return isError, hasChanged, meta

def server_group_stop(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    exists = isServerGroupAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}

    if exists:
        cli1 = "/server-group=%s:stop-servers" % (data['server_group_name'])
        p = subprocess.Popen(["sh", cmd, "-c", cli1, controller], stdout=subprocess.PIPE)
        result,err = p.communicate()
        meta = {"status": "OK", "response": result}
    else:
        hasChanged = False
        resp = "Server group %s does not exist" % (data['server_group_name'])
        meta = {"status" : "OK", "response" : resp}

    return isError, hasChanged, meta

def main():

    fields = {
        "jboss_home" : {"required": True, "type": "str"},
        "server_group_name": {"required": True, "type": "str"},
        "server_group_profile": {
            "required": False,
            "default": "default",
            "type": "str"
        },
        "socket_binding_group": {
            "required": False,
            "default": "standard-sockets",
            "type": "str"
        },
        "controller_host": {
            "required": False,
            "default": "localhost",
            "type": "str"
        },
        "controller_port": {
            "required": False,
            "default": 9990,
            "type": "int"
        },
        "state": {
            "default": "present",
            "choices": ['present', 'absent', 'start', 'stop'],
            "type": 'str'
        },
    }

    choice_map = {
        "present": server_group_present,
        "absent": server_group_absent,
        "start": server_group_start,
        "stop": server_group_stop
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
        module.params['state'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error creating server group", meta=result)

if __name__ == '__main__':
    main()
