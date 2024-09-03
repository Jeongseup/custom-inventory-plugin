from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: ssh_config_plugin
    plugin_type: inventory
    short_description: Returns Ansible inventory from SSH config files
    description:
      - Reads SSH config files from ~/.ssh/config.d and creates an inventory.
      - Groups hosts based on the hostname structure by splitting on '-'.
    options:
      plugin:
          description: Name of the plugin
          required: true
          choices: ['ssh_config_plugin']
      ssh_config_dir:
        description: Directory location of SSH config.d
        required: true
'''

from ansible.plugins.inventory import BaseInventoryPlugin # type: ignore
from ansible.errors import AnsibleParserError # type: ignore
import glob
import os

class InventoryModule(BaseInventoryPlugin):
    NAME = 'ssh_config_plugin'

    def verify_file(self, path):
        '''Return true/false if this is possibly a valid file for this plugin to consume'''
        # valid = False
        # if super(InventoryModule, self).verify_file(path):
        #     if path.endswith(('ssh_inventory.yaml', 'ssh_inventory.yml')):
        #         valid = True
        # return valid
        return True
    
    def parse(self, inventory, loader, path, cache):
        '''Return dynamic inventory from source '''
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        # Read the inventory YAML file
        self._read_config_data(path)
        try:
            # Store the options from the YAML file            
            self.plugin = self.get_option('plugin')
            self.ssh_config_dir = self.get_option('ssh_config_dir')
        except Exception as e:
            raise AnsibleParserError(f"All required options not found: {e}")
        # Populate the inventory
        self._populate()

    def _get_ssh_config_data(self, ssh_config_dir):
        '''Read SSH config files and return structured inventory data'''
        hosts = []
        for config_file in glob.glob(os.path.join(ssh_config_dir, '*')):
            with open(config_file, 'r') as f:
                lines = f.readlines()

            host_info = {}
            for line in lines:
                if line.startswith("Host "):
                    parts = line.split()
                    if len(parts) > 1:  # Ensure there is at least one element after "Host"
                        if 'ip' in host_info and host_info['ip']:  # Save previous host information only if 'ip' exists and is not empty
                            hosts.append(host_info)
                        host_info = {}
                        host_info['hostname'] = parts[1]
                elif line.startswith("HostName "):
                    parts = line.split()
                    if len(parts) > 1:  # Ensure there is at least one element after "HostName"
                        host_info['ip'] = parts[1]
                elif line.startswith("User "):
                    parts = line.split()
                    if len(parts) > 1:  # Ensure there is at least one element after "User"
                        host_info['user'] = parts[1]

            if 'ip' in host_info and host_info['ip']:  # Save last host information
                hosts.append(host_info)

        return hosts

    def _populate(self):
        '''Create groups and add hosts to the inventory based on the SSH config data'''
        ssh_config_dir = os.path.expanduser(self.ssh_config_dir)
        hosts = self._get_ssh_config_data(ssh_config_dir)

        # NOTE: if enable this, you can derive into debug mode
        # import pdb; pdb.set_trace()

        for host_info in hosts:
            hostname = host_info['hostname']
            ip = host_info.get('ip', '')
            user = host_info.get('user', '')

            # Split hostname by '-'
            parts = hostname.split('-')

            # Define group names based on the hostname structure
            if len(parts) >= 4:
                environment = parts[0]  # e.g., 'p'
                provider = parts[1]     # e.g., 'aws'
                location = parts[2]     # e.g., 'seoul'
                role = parts[3]         # e.g., 'node'

                # Add groups if they don't already exist
                self.inventory.add_group(environment)
                self.inventory.add_group(provider)
                self.inventory.add_group(location)
                self.inventory.add_group(role)

                # Add the host to the appropriate groups
                self.inventory.add_host(hostname, group=environment)
                self.inventory.add_host(hostname, group=provider)
                self.inventory.add_host(hostname, group=location)
                self.inventory.add_host(hostname, group=role)

                # Set host variables
                self.inventory.set_variable(hostname, 'ansible_host', ip)
                self.inventory.set_variable(hostname, 'ansible_user', user)        
