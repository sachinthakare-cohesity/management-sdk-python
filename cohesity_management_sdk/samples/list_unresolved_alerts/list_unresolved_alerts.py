# Copyright 2019 Cohesity Inc.
#
# Python example to list recent user_configurable unresolved alert unresolved Alerts.
# This script is compatible with both Python2 and Python3
# Usage: python list_unresolved_alerts.py --max_alerts 10

import os
import argparse
import datetime

from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.models.alert_state_list_enum \
    import AlertStateListEnum

MAX_ALERTS = 100

class Alerts(object):
    """
    Class to display Alerts.
    """
    severity_map = {'kCritical':'CRITICAL', 'kWarning':'WARNING',
                    'kInfo':'INFO'}
    category_map = {'kDisk':'DISK', 'kNode': 'NODE', 'kCluster': 'CLUSTER',
                    'kNodeHealth': 'NODE_HEALTH',
                    'kClusterHealth': 'CLUSTER_HEALTH',
                    'kBackupRestore': 'BACKUP_RESTORE',
                    'kEncryption':'ENCRYPTION',
                    'kArchivalRestore': 'ARCHIVAL_RESTORE'}

    def display_alerts(self, cohesity_client, max_alerts):
        """
        Method to display the list of Unresolved Alerts
        :param cohesity_client(object): Cohesity client object.
        :return:
        """
        alerts = cohesity_client.alerts
        alerts_list = alerts.get_alerts(max_alerts=max_alerts,
                                        alert_state_list=
                                        [AlertStateListEnum.KOPEN])
        for alert in alerts_list:
            print ('{0:<10}\t\t{1:>8}\t{2:>10}'.
                   format(self.epoch_to_date(alert.first_timestamp_usecs),
                          self.category_map[alert.alert_category],
                          self.severity_map[alert.severity]))

    @staticmethod
    def epoch_to_date(epoch):
        """
        Method to convert epoch time in usec to date format
        :param epoch(int): Epoch time of the job run.
        :return: date(str): Date format of the job run.
        """
        date_string = datetime.datetime.fromtimestamp(epoch/10**6).\
            strftime('%m-%d-%Y %H:%M:%S')
        return date_string


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
    parser.add_argument("--max_alerts", help="Number of Alerts.",
                        default=MAX_ALERTS)
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

    alerts = Alerts()
    alerts.display_alerts(cohesity_client, args.max_alerts)


if __name__ == '__main__':
    main()
