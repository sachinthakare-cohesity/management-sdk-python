# -*- coding: utf-8 -*-
# Copyright 2019 Cohesity Inc.

import logging
from cohesity_management_sdk.api_helper import APIHelper
from cohesity_management_sdk.configuration import Configuration
from cohesity_management_sdk.controllers.base_controller import BaseController
from cohesity_management_sdk.http.auth.auth_manager import AuthManager
from cohesity_management_sdk.models.privilege_information import PrivilegeInformation
from cohesity_management_sdk.exceptions.error_error_exception import ErrorErrorException

class Privileges(BaseController):

    """A Controller to access Endpoints in the cohesity_management_sdk API."""

    def __init__(self, client=None, call_back=None):
        super(Privileges, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def get_privileges(self,
                       name=None):
        """Does a GET request to /public/privileges.

        If the 'name' parameter is not specified, all privileges defined
        on the Cohesity Cluster are returned.
        In addition, information about each privilege is returned such as the
        associated category, description, name,  etc.
        If an exact privilege name (such as PRINCIPAL_VIEW) is specified in
        the
        'name' parameter, only information about that single privilege is
        returned.

        Args:
            name (string, optional): Specifies the name of the privilege.

        Returns:
            list of PrivilegeInformation: Response from the API. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_privileges called.')

            # Prepare query URL
            self.logger.info('Preparing query URL for get_privileges.')
            _url_path = '/public/privileges'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'name': name
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)

            # Prepare headers
            self.logger.info('Preparing headers for get_privileges.')
            _headers = {
                'accept': 'application/json'
            }

            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_privileges.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request)
            _context = self.execute_request(_request, name = 'get_privileges')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_privileges.')
            if _context.response.status_code == 0:
                raise ErrorErrorException('Error', _context)
            self.validate_response(_context)

            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, PrivilegeInformation.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
