# -*- coding: utf-8 -*-
# Copyright 2019 Cohesity Inc.

import cohesity_management_sdk.models.bandwidth_limit
import cohesity_management_sdk.models.create_access_token_credential_request
import cohesity_management_sdk.models.storage_domain_view_box_pairing

class RegisterRemoteCluster(object):

    """Implementation of the 'Register Remote Cluster.' model.

    Specifies the settings required for registering a remote Cluster
    on this local Cluster.

    Attributes:
        all_endpoints_reachable (bool): Specifies whether any endpoint (such
            as a Node) on the remote Cluster is reachable from this local
            Cluster. If true, a service running on the local Cluster can
            communicate directly with any of its peers running on the remote
            Cluster, without using a proxy.
        bandwidth_limit (BandwidthLimit): Specifies settings for limiting the
            data transfer rate between the local and remote Clusters.
        clear_interfaces (bool): TODO: type description here.
        clear_vlan_id (bool): Specifies whether to clear the vlanId field, and
            thus stop using only the IPs in the VLAN for communicating with
            the remote Cluster.
        cluster_id (long|int): Specifies the unique id of the remote Cluster.
        compression_enabled (bool): Specifies whether to compress the outbound
            data when transferring the replication data over the network to
            the remote Cluster.
        encryption_key (string): Specifies the encryption key used for
            encrypting the replication data from a local Cluster to a remote
            Cluster. If a key is not specified, replication traffic encryption
            is disabled. When Snapshots are replicated from a local Cluster to
            a remote Cluster, the encryption key specified on the local
            Cluster must be the same as the key specified on the remote
            Cluster.
        iface_name (string): Specifies the interface name of the VLAN to use
            for communicating with the remote Cluster.
        network_interface_group (string): Specifies the group name of the
            network interfaces to use for communicating with the remote
            Cluster.
        network_interface_ids (list of long|int): Array of Network Interface
            Ids.  Specifies the ids of the network interfaces to use for
            communicating with the remote Cluster.
        password (string): Specifies the password for Cohesity user to use
            when connecting to the remote Cluster.
        purpose_remote_access (bool): Whether the remote cluster will be used
            for remote access for SPOG.
        purpose_replication (bool): Whether the remote cluster will be used
            for replication.
        remote_access_credentials (CreateAccessTokenCredentialRequest):
            Specifies the Cohesity credentials required for generating an
            access token.
        remote_ips (list of string): Array of Remote Node IP Addresses.
            Specifies the IP addresses of the Nodes on the remote Cluster to
            connect with. These IP addresses can also be VIPS. Specifying
            hostnames is not supported.
        remote_iris_ports (list of long|int): Array of Ports.  Specifies the
            ports to use when connecting to the Nodes of the remote Cluster.
        user_name (string): Specifies the Cohesity user name used to connect
            to the remote Cluster.
        validate_only (bool): Whether to only validate the credentials without
            saving the information.
        view_box_pair_info (list of StorageDomainViewBoxPairing): Array of
            Storage Domain (View Box) Pairs.  Specifies pairings between
            Storage Domains (View Boxes) on the local Cluster with Storage
            Domains (View Boxes) on a remote Cluster that are used in
            replication.
        vlan_id (int): Specifies the Id of the VLAN to use for communicating
            with the remote Cluster.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "all_endpoints_reachable":'allEndpointsReachable',
        "bandwidth_limit":'bandwidthLimit',
        "clear_interfaces":'clearInterfaces',
        "clear_vlan_id":'clearVlanId',
        "cluster_id":'clusterId',
        "compression_enabled":'compressionEnabled',
        "encryption_key":'encryptionKey',
        "iface_name":'ifaceName',
        "network_interface_group":'networkInterfaceGroup',
        "network_interface_ids":'networkInterfaceIds',
        "password":'password',
        "purpose_remote_access":'purposeRemoteAccess',
        "purpose_replication":'purposeReplication',
        "remote_access_credentials":'remoteAccessCredentials',
        "remote_ips":'remoteIps',
        "remote_iris_ports":'remoteIrisPorts',
        "user_name":'userName',
        "validate_only":'validateOnly',
        "view_box_pair_info":'viewBoxPairInfo',
        "vlan_id":'vlanId'
    }

    def __init__(self,
                 all_endpoints_reachable=None,
                 bandwidth_limit=None,
                 clear_interfaces=None,
                 clear_vlan_id=None,
                 cluster_id=None,
                 compression_enabled=None,
                 encryption_key=None,
                 iface_name=None,
                 network_interface_group=None,
                 network_interface_ids=None,
                 password=None,
                 purpose_remote_access=None,
                 purpose_replication=None,
                 remote_access_credentials=None,
                 remote_ips=None,
                 remote_iris_ports=None,
                 user_name=None,
                 validate_only=None,
                 view_box_pair_info=None,
                 vlan_id=None):
        """Constructor for the RegisterRemoteCluster class"""

        # Initialize members of the class
        self.all_endpoints_reachable = all_endpoints_reachable
        self.bandwidth_limit = bandwidth_limit
        self.clear_interfaces = clear_interfaces
        self.clear_vlan_id = clear_vlan_id
        self.cluster_id = cluster_id
        self.compression_enabled = compression_enabled
        self.encryption_key = encryption_key
        self.iface_name = iface_name
        self.network_interface_group = network_interface_group
        self.network_interface_ids = network_interface_ids
        self.password = password
        self.purpose_remote_access = purpose_remote_access
        self.purpose_replication = purpose_replication
        self.remote_access_credentials = remote_access_credentials
        self.remote_ips = remote_ips
        self.remote_iris_ports = remote_iris_ports
        self.user_name = user_name
        self.validate_only = validate_only
        self.view_box_pair_info = view_box_pair_info
        self.vlan_id = vlan_id


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        all_endpoints_reachable = dictionary.get('allEndpointsReachable')
        bandwidth_limit = cohesity_management_sdk.models.bandwidth_limit.BandwidthLimit.from_dictionary(dictionary.get('bandwidthLimit')) if dictionary.get('bandwidthLimit') else None
        clear_interfaces = dictionary.get('clearInterfaces')
        clear_vlan_id = dictionary.get('clearVlanId')
        cluster_id = dictionary.get('clusterId')
        compression_enabled = dictionary.get('compressionEnabled')
        encryption_key = dictionary.get('encryptionKey')
        iface_name = dictionary.get('ifaceName')
        network_interface_group = dictionary.get('networkInterfaceGroup')
        network_interface_ids = dictionary.get('networkInterfaceIds')
        password = dictionary.get('password')
        purpose_remote_access = dictionary.get('purposeRemoteAccess')
        purpose_replication = dictionary.get('purposeReplication')
        remote_access_credentials = cohesity_management_sdk.models.create_access_token_credential_request.CreateAccessTokenCredentialRequest.from_dictionary(dictionary.get('remoteAccessCredentials')) if dictionary.get('remoteAccessCredentials') else None
        remote_ips = dictionary.get('remoteIps')
        remote_iris_ports = dictionary.get('remoteIrisPorts')
        user_name = dictionary.get('userName')
        validate_only = dictionary.get('validateOnly')
        view_box_pair_info = None
        if dictionary.get('viewBoxPairInfo') != None:
            view_box_pair_info = list()
            for structure in dictionary.get('viewBoxPairInfo'):
                view_box_pair_info.append(cohesity_management_sdk.models.storage_domain_view_box_pairing.StorageDomainViewBoxPairing.from_dictionary(structure))
        vlan_id = dictionary.get('vlanId')

        # Return an object of this model
        return cls(all_endpoints_reachable,
                   bandwidth_limit,
                   clear_interfaces,
                   clear_vlan_id,
                   cluster_id,
                   compression_enabled,
                   encryption_key,
                   iface_name,
                   network_interface_group,
                   network_interface_ids,
                   password,
                   purpose_remote_access,
                   purpose_replication,
                   remote_access_credentials,
                   remote_ips,
                   remote_iris_ports,
                   user_name,
                   validate_only,
                   view_box_pair_info,
                   vlan_id)


