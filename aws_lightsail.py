#!/usr/bin/env python3

'''
Custom dynamic inventory script for AWS Lightsail.
@3sky

User need to provide:
- AWS_KEY_ID
- AWS_ACCESS_KEY
- ENV_TAG

as environment variables
export AWS_KEY_ID=xxxx
export AWS_ACCESS_KEY=xxx
export ENV_TAG=xxx
'''

import os
import sys
import argparse

try:
    import json
except ImportError:
    import simplejson as json

try:
    import boto3
    import botocore
except ImportError:
    print("Install boto3 first - pip3 install boto3 botocore")
    os.exit()

class LightsailInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        if self.args.list:
            ## set tags for checking machines
            self.inventory = self.lightsail_inventory(os.environ['ENV_TAG'])
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory));


    def lightsail_inventory(self, input_tag):

        try:
            client = boto3.client(
                'lightsail',
                aws_access_key_id=os.environ['AWS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_ACCESS_KEY'],
                region_name='eu-central-1'
            )

        except botocore.exceptions.ClientError as error:
            print("AWS auth problem")
            os.exit()
            raise error

        response = client.get_instances()
        machine_list = {'lightsail_group': {'hosts': [], 'vars': {'ansible_ssh_user': 'ubuntu'}}}
        for instance in response['instances']:
            for tag in instance['tags']:
                if tag['key'] == input_tag:
                    machine_list['lightsail_group']['hosts'].append(instance['publicIpAddress'])
        return machine_list

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
LightsailInventory()
