# Copyright 2019 Cohesity Inc.
#
# Python example to start a protection job on demand by job name.
# This script is compatible with Python2
# Usage: python on_demand_job_run.py --job_name <name_of_protection_job>

import os
import argparse
import time

from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.protection_run_parameters \
    import ProtectionRunParameters
from cohesity_management_sdk.models.run_type_2_enum import RunType2Enum
from cohesity_management_sdk.models.run_status_enum import RunStatusEnum
from cohesity_app_sdk.app_client import AppClient


class ProtectionJobs(object):
    """
    Class to display Alerts.
    """

    def __init__(self, cclient):
        self.cohesity_client = cclient
        self.jobs_controller = self.cohesity_client.protection_jobs
        self.run_controller = self.cohesity_client.protection_runs

    def name_to_job_id(self, job_name):
        """
        Method to convert name of the job to id. If conflicts
        :param job_name(str): Name of the Protection job.
        :return
            status(bool): If Protection job doesn't exist,
            this is set to False.
            job_id(int) : Protection Job ID.
        """
        result = self.jobs_controller.get_protection_jobs(names=job_name)
        if not result:
            return False, 0
        return True, result[0].id

    def run_job(self, job_name):
        """
        Method to run the Job specified on demand.
        :param job_name(str): Protection Job name.
        :return: None.
        """
        status, job_id = self.name_to_job_id(job_name)
        if not status:
            print ("Protection Job with name: %s doesn't exist" % job_name)
            exit(0)

        req_body = ProtectionRunParameters()
        req_body.run_type = RunType2Enum.KREGULAR
        self.jobs_controller.create_run_protection_job(id=job_id,
                                                       body=req_body)

        # Get the status of this Job run.
        jresp = self.run_controller.get_protection_runs(job_id=job_id,
                                                        num_runs=1)
        if jresp == []:
            time.sleep(20)
            jresp = self.run_controller.get_protection_runs(job_id=job_id,
                                                            num_runs=1)[0]
        else:
            jresp = jresp[0]
        if jresp.backup_run.status == RunStatusEnum.KSUCCESS:
            print ("Protection Job %s started successfully" % job_name)
        elif jresp.backup_run.status == RunStatusEnum.KERROR:
            print ("Protection Job %s failed." % job_name)


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

    pj = ProtectionJobs(cohesity_client)
    pj.run_job(args.job_name)


if __name__ == '__main__':
    main()
