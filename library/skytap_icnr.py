#!/usr/bin/python
# Copyright (c) 2016 Ben Coleman
# Software provided under the terms of the Apache 2.0 license http://www.apache.org/licenses/LICENSE-2.0.txt

DOCUMENTATION = '''
---
module: skytap_icnr
short_description: Connect environments via ICNR tunnels
'''

import json
import requests
import sys
import time
from ansible.module_utils.basic import AnsibleModule

# API endpoint for Skytap REST API
API_BASE = 'https://cloud.skytap.com/'
API_HEADERS = {'accept': 'application/json', 'content-type': 'application/json'}
BACKOFF_DELAY = 6
retries = 5

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
    global retries
    module = AnsibleModule(
        argument_spec = dict(
            username = dict(required=True),
            token = dict(required=True),
            action = dict(default='create', choices=['create', 'delete']),
            source_net_id = dict(required=True),
            target_net_id = dict(required=True),
        ),
        supports_check_mode=False
    )
    auth = (module.params.get('username'), module.params.get('token'))

    if module.params.get('action') == 'create':
        request_data = {"source_network_id": module.params.get('source_net_id'), "target_network_id": module.params.get('target_net_id')}
        status, result = restCall(auth, 'POST', '/v2/tunnels', data=json.dumps(request_data))

    # Check for rate limiting and retry
    if (status == 423 or status == 429) and retries > 0:
        retries = retries - 1
        time.sleep(BACKOFF_DELAY)
        main()

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
