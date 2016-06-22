#!/usr/bin/python
# Copyright (c) 2016 Ben Coleman
# Software provided under the terms of the Apache 2.0 license http://www.apache.org/licenses/LICENSE-2.0.txt

DOCUMENTATION = '''
---
module: skytap_template
short_description: Manage Skytap templates
'''

import json
import requests
import sys
import time
from ansible.module_utils.basic import AnsibleModule

# API endpoint for Skytap REST API
API_BASE = 'https://cloud.skytap.com/'
API_HEADERS = {'accept': 'application/json', 'content-type': 'application/json'}

#  Basic REST call to Skytap API
def restCall(auth, method, path, data=None):
    try:
        if(method == 'GET'):
            result = requests.get(API_BASE + path, headers=API_HEADERS, auth=auth)
        if(method == 'POST'):
            result = requests.post(API_BASE + path, headers=API_HEADERS, auth=auth, data=data)
        if(method == 'PUT'):
            result = requests.put(API_BASE + path, headers=API_HEADERS, auth=auth, data=data)
        if(method == 'DELETE'):
            result = requests.delete(API_BASE + path, headers=API_HEADERS, auth=auth, allow_redirects=True)

        if len(result.content) > 0:
            return result.status_code, result.json()
        else:
            return result.status_code, None
    except:
        return -1, None

# Main module code here
def main():
    module = AnsibleModule(
        argument_spec = dict(
            username = dict(required=True),
            token = dict(required=True),
            action = dict(default='create', choices=['create', 'modify', 'delete', 'list']),
            template_id = dict(required=False),
            environment_id = dict(required=False),
            name = dict(required=False),
            owner_id = dict(required=False),
        ),
        supports_check_mode=False
    )
    auth = (module.params.get('username'), module.params.get('token'))

    if module.params.get('action') == 'create':
        if not module.params.get('environment_id'):
            module.fail_json(msg="environment_id is required param when action=create")
        request_data = {"configuration_id": module.params.get('environment_id')}
        if module.params.get('name'):
            request_data['name'] = module.params.get('name')

        status, result = restCall(auth, 'POST', '/v1/templates', data=json.dumps(request_data))

    if module.params.get('action') == 'modify':
        if not module.params.get('template_id'):
            module.fail_json(msg="template_id is required param when action=modify")
        request_data = {}
        if module.params.get('name'):
            request_data['name'] = module.params.get('name')
        if module.params.get('owner_id'):
            request_data['owner'] = module.params.get('owner_id')

        status, result = restCall(auth, 'PUT', '/v1/templates/' + str(module.params.get('template_id')), data=json.dumps(request_data))

    if module.params.get('action') == 'delete':
        if not module.params.get('template_id'):
            module.fail_json(msg="template_id is required param when action=delete")

        status, result = restCall(auth, 'DELETE', '/v1/templates/' + str(module.params.get('template_id')))

    if module.params.get('action') == 'list':
        status, result = restCall(auth, 'GET', '/v2/templates?scope=me&count=100')

    # Check results and exit
    if status != requests.codes.ok:
        err = "No error message given, likely connection or network failure"
        if result != None and result.has_key('error'): err = result['error']
        module.fail_json(msg="API call failed, HTTP status: "+str(status)+", error: "+err)
    else:
        module.exit_json(changed=True, api_result=result, status_code=status)

    module.exit_json(changed=False)

if __name__ == '__main__':
    main()
