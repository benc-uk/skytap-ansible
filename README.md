# Skytap Ansible Integration

Custom modules for Ansible for working with Skytap Cloud. Included are some example playbooks demonstrating usage

### Overview
This is a set of modules for integrating Skytap with Ansible. 
Four modules are provided and each has a range of actions in Skytap they can carry out. All modules are wrappers around the standard REST API

### Basic usage and Pre-reqs
Pre-reqs:
 - A working Ansible deployment. It has been tested with Ansible deployed in Skytap, but this is not a requirement
 - Skytap account with username and [your API token](http://help.skytap.com/kb-find-api-token.html)

Getting started:
 - Clone this repo to somewhere on your Ansible server, e.g. `/home/cooldude/skytap-ansible/`
 - Add this path to the Ansible custom library path:
   * Edit `/etc/anisble/ansible.cfg` and add **`library = /home/cooldude/skytap-ansible/library`**
   * Set env variable. `export ANSIBLE_LOCAL_TEMP=/home/cooldude/skytap-ansible/library`
 - Before running the example playbooks, edit the example vars in `/home/cooldude/skytap-ansible/vars/example.yml` Set values as befitting your Skytap account
 - Run example playbook e.g. `ansible-playbook environment_example.yml -vvvv`
 - Look on in wonder as cloud environments are dynamically controlled from your boring old Ansible playbook

### Module names and actions
 - **skytap_environment** - For working with Skytap environments. Supported actions: 'create', 'modify', 'delete', 'read', 'list', 'wait_ratelimit', 'copy'. Wrapper around the `https://cloud.skytap.com/v1/configurations/` API resource 
 
 - **skytap_template** - For working with Skytap templates. Suported actions: 'create', 'modify', 'delete', 'list', 'copy', 'read'. Wrapper around the `https://cloud.skytap.com/v1/templates/` API resource 
 
 - **skytap_project** - For working with Skytap projects. Suported actions: 'create', 'delete', 'list', 'read', 'list_users', 'add_env', 'add_asset', 'add_template'. Wrapper around the `https://cloud.skytap.com/v1/projects/` API resource 
 
 - **skytap_icnr** - For working with Skytap inter-configuration network tunnels (ICNR). Suported actions: 'create', 'delete'. Wrapper around the `https://cloud.skytap.com/v1/templates/` API resource 
