# Copyright 2019 Cohesity Inc.
#
# Python example to add a VM to a protection Job.
# This script is compatible with Python2
# Usage: python register_vcenter.py

import os
import argparse
from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.environment_enum import EnvironmentEnum
from cohesity_management_sdk.models.vmware_type_enum import VmwareTypeEnum
from cohesity_management_sdk.models.register_protection_source_parameters \
    import RegisterProtectionSourceParameters


CLUSTER_USERNAME = 'cluster_username'
CLUSTER_PASSWORD = 'cluster_password'
CLUSTER_VIP = 'prod-cluster.cohesity.com'
VCENTER_IP = 'vcenter_ip'
VCENTER_USERNAME = 'administrator'
VCENTER_PASSWORD = 'vcenter_password'

class AddVCenter(object):

    def __init__(self, cohesity_client):
        self.cohesity_client = cohesity_client

    def register_vcenter(self):
        """
        Method to register vcenter.
        :return True, False.
        """
        req_body = RegisterProtectionSourceParameters()
        req_body.endpoint = VCENTER_IP
        req_body.username = VCENTER_USERNAME
        req_body.password = VCENTER_PASSWORD
        req_body.environment = EnvironmentEnum.K_VMWARE
        req_body.vmware_type = VmwareTypeEnum.KVCENTER
        source = self.cohesity_client.protection_sources
        source.create_register_protection_source(req_body)
        print("Successfully Registered the vCenter.")

def get_mgnt_token():
    """
    To get the management access token from athena to authenticate
    :return: mgmt_auth_token
    """
    # Get the Environment variables from App Container.
    app_auth_token = os.getenv('APP_AUTHENTICATION_TOKEN')
    app_endpoint_ip = os.getenv('APPS_API_ENDPOINT_IP')
    app_endpoint_port = os.getenv('APPS_API_ENDPOINT_PORT')


    # Initialize the client.
    app_cli = AppClient(app_auth_token, app_endpoint_ip, app_endpoint_port)
    app_cli.config.disable_logging()

    # Get the settings information.
    settings = app_cli.settings
    print(settings.get_app_settings())

    # Get the management access token.
    token = app_cli.token_management
    mgmt_auth_token = token.create_management_access_token()
    return mgmt_auth_token

def get_cmdl_args():
    """"
    To accept all commandline arguments eg userId and password
    """
    parser = argparse.ArgumentParser(description="Arguments needed to run "
                                                 "python scripts eg. "
                                                 "cluster_vip,"
                                                 "UserName & Password")
    parser.add_argument("-i", "--cluster_vip", help="Cluster VIP to login")
    parser.add_argument("-u", "--user", help="Username to login")
    parser.add_argument("-p", "--password", help="password to login")
    args = parser.parse_args()
    return args


def main():
    # Login to the cluster
    args = get_cmdl_args()
    if args.cluster_vip is not None and args.user is not None and \
    args.password is not None:
        cohesity_client = CohesityClient(cluster_vip=args.cluster_vip,
                                         username=args.user,
                                         password=args.password)
    elif args.cluster_vip is not None or args.user is not None or \
    args.password is not None:
        print("Please provide all inputs ie. cluster_vip, user & password")
        exit()
    else:
        host_ip = os.getenv('HOST_IP')
        mgmt_auth_token = get_mgnt_token()
        cohesity_client = CohesityClient(cluster_vip=host_ip,
                                         auth_token=mgmt_auth_token)

    vcenter_object = AddVCenter(cohesity_client)
    vcenter_object.register_vcenter()


if __name__ == '__main__':
    main()
