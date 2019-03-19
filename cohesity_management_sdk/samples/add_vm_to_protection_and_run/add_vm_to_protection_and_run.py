# Copyright 2019 Cohesity Inc.
#
# This script is compatible with Python2
#
# Python example to add a VM to a protection Job.
# Note: This script assumes you have a vCenter as a protection source in your
# Cohesity Cluster.
# Usage: python add_vm_to_protection_and_run.py \
# --job_name=<name_of_protection_job> --vm_list=<list_of_vms> --run_now=True

import os
import argparse

from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.samples.on_demand_job_run.on_demand_job_run \
    import ProtectionJobs
from cohesity_app_sdk.app_client import AppClient


class AddVMProtectionJob(object):

    def __init__(self, cohesity_client):
        self.cohesity_client = cohesity_client

    def add_to_protection_job(self, vm_list, pjob_name):
        """
        Method to add VM list to the protection Job.
        :param vm_list(list): List of VMs to be protected.
        :param pj_name(str): Name of protection job.
        :return: None
        """

        # Check if vm's exists
        vm_id_list = self.check_vms_exists(vm_list)

        # Check if protection job exists.
        status, resp = self.check_protection_job_exists(pjob_name)
        if not status:
            print ("\n\n *Protection Job Name not in system*\n\n")
            exit()

        # Add the vms to the protection job.
        resp.source_ids = vm_id_list + resp.source_ids
        update_resp = self.cohesity_client.protection_jobs.\
            update_protection_job(body=resp, id=resp.id)
        assert update_resp.source_ids == resp.source_ids, \
            "Failed to add VMs to Protection Jobs."
        print("VM(s) %s added to protection job successfully" % vm_list)

    def check_vms_exists(self, vm_list):
        """
        Method to check if VM exists
        :return:
        """
        str_vm_list = ','.join(vm_list)
        # Note: This API works only with vCenter VMs.
        print(str_vm_list)
        resp_vm_list = self.cohesity_client.protection_sources\
            .list_virtual_machines(names=str_vm_list)

        assert len(vm_list) == len(resp_vm_list), "VMs not found " \
                                                  "in the vCenter."
        return [vm.id for vm in resp_vm_list]


    def check_protection_job_exists(self,protect_job_name):
        """
        Method to check if protection job exists.
        :param pj_name(str): Name of Protection Job.
        :return
            Boolean: Return True if exists, else return False.
            job_id(int): Protection job ID.
        """
        pj_list = self.cohesity_client.protection_jobs.\
            get_protection_jobs(only_return_basic_summary=True)
        for job in pj_list:
            if job.name == protect_job_name:
                return True, job
        return False, None

def get_mgnt_token():
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
    parser = argparse.ArgumentParser(description="Arguments needed to run "
                                                 "python scripts eg. "
                                                 "cluster_vip,"
                                                 "UserName & Password")
    parser.add_argument("-i", "--cluster_vip", help="Cluster VIP to login")
    parser.add_argument("-u", "--user", help="Username to login")
    parser.add_argument("-p", "--password", help="password to login")
    args = parser.parse_args()
    return args

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
    parser.add_argument("--job_name", help="Name of the Protection Job.",
                        required=True)
    parser.add_argument("--vm_list", help="Name of the VM to be added to "
                                          "Protection Job.", required=True,
                        type=str)
    parser.add_argument("--run_now", help="Specify True to run job now.",
                        default=False, type=bool)

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

    cohesity_client.config.cluster_vip = args.cluster_vip
    vm_protect = AddVMProtectionJob(cohesity_client)

    # add those vms to a protection job
    vm_list = [str(item) for item in args.vm_list.split(',')]
    vm_protect.add_to_protection_job(vm_list, args.job_name)

    # Run protection job on demand. from other file.
    if args.run_now:
        protect_object = ProtectionJobs(cohesity_client)
        protect_object.run_job(args.job_name)
        print("Protection Job run successfully")


if __name__ == '__main__':

    main()
