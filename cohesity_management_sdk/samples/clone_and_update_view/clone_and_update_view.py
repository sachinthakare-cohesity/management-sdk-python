# Copyright 2019 Cohesity Inc.
#
# This script is compatible with both Python2 and Python3
#
# Python example to
#   1. clone an existing view.
#   2. Update the cloned view.
# Usage: python clone_and_update_view.py --view_name=<name_of_view> \
# --clone_name=<cloned_view_name>

import os
import argparse
import json
import jsonpickle
import pprint
import random
import string

from cohesity_management_sdk.cohesity_client import CohesityClient
from cohesity_management_sdk.exceptions.api_exception import APIException
from cohesity_management_sdk.models.protocol_access_enum \
    import ProtocolAccessEnum
from cohesity_management_sdk.models.view import View


class CloneView(object):
    """
    Class to list the protection jobs.
    """

    def __init__(self, cohesity_client):
        self.view_client = cohesity_client.views

    def clone_existing_view(self, view_name, clone_name):
        """
        Method to clone the view.
        :param cohesity_client(obj): Cohesity Rest API client.
        :param view_name(str): View name.
        :param clone_name(str): Clone view name.
        :return None.
        """
        json_req = {"cloneViewName": clone_name, "sourceViewName": view_name}
        resp = self.view_client.create_clone_view(body=json_req)
        print ("Cloned view:")
        cloned_view = jsonpickle.encode(resp)
        pprint.pprint(json.loads(cloned_view))
        return cloned_view

    def update_view(self, view_name, protocol_access, description):
        """
        Method to update the existing view with different protocol
        & description
        :param view_name(str): Name of the view.
        :param protocol_access(str): Valid values: [ kAll, kNFSOnly,
                    kSMBOnly, kS3Only ]
        :param description(str): User defined description for the view.
        :return None.
        """
        req_json = View()
        req_json.description = description
        req_json.protocol_access = protocol_access
        resp = self.view_client.update_view_by_name(body=req_json,
                                                    name=view_name)
        updated_view = json.loads(jsonpickle.encode(resp))

        # Verify the fields updated
        assert updated_view['protocol_access']== protocol_access,\
            "View not updated"
        assert updated_view['description'] == description, "View not updated"
        print ("Updated view:")
        pprint.pprint(updated_view)

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
    parser.add_argument("--view_name", help="Name of the View to clone.",
                        required=True)
    parser.add_argument("--clone_name", help="Clone view name.",
                        required=False)

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

    view_name = args.view_name
    clone_name = args.clone_name

    if args.clone_name is None:
        clone_name = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(5)) + \
                     '_cloned_view_' + args.view_name

    # Clone a view with name.
    try:
        cloneview = CloneView(cohesity_client)
        cloneview.clone_existing_view(view_name, clone_name)

        # Update the cloned view.
        cloneview.update_view(view_name=clone_name,
                              protocol_access=ProtocolAccessEnum.KNFSONLY,
                              description="View to restrict access"
                                          " to s3 only.")
    except APIException as e:
        print("Error : %s" % e.context.response.raw_body)


if __name__ == '__main__':
    main()
