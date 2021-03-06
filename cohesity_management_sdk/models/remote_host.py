# -*- coding: utf-8 -*-
# Copyright 2019 Cohesity Inc.


class RemoteHost(object):

    """Implementation of the 'Remote Host.' model.

    Specifies the settings required to connect to a remote host.

    Attributes:
        address (string): Specifies the address (IP, hostname or FQDN) of the
            remote host that will run the script.
        mtype (Type24Enum): Specifies the OS type of the remote host that will
            run the script. Currently only 'kLinux' is supported. 'kLinux'
            indicates the Linux operating system. 'kWindows' indicates the
            Microsoft Windows operating system. 'kAix' indicates the IBM AIX
            operating system. 'kSolaris' indicates the Oracle Solaris
            operating system.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "address":'address',
        "mtype":'type'
    }

    def __init__(self,
                 address=None,
                 mtype=None):
        """Constructor for the RemoteHost class"""

        # Initialize members of the class
        self.address = address
        self.mtype = mtype


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
        address = dictionary.get('address')
        mtype = dictionary.get('type')

        # Return an object of this model
        return cls(address,
                   mtype)


