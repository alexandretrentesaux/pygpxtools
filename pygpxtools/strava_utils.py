# -*- encoding: utf-8 -*-

import configparser
import tempfile
import os
import sys
from pygpxtools.__init__ import __logger__



# create connection config file
def strava_configure(client_id, client_secret, token):
    """Create config file with connections parameters

    Args:
        client_id (str): Strava API client ID
        client_secret (str): Strava API client secret
        token (str): Strava API app token
    """
    config = configparser.RawConfigParser()
    config.add_section('default')
    config.set('default', 'client_id', str(client_id))
    config.set('default', 'client_secret', str(client_secret))
    config.set('default', 'token', str(token))
    with open(os.path.join(tempfile.gettempdir(), 'pyrbw.ini'), 'w+') as config_file:
        config.write(config_file)


# get strava auth info from config file
def strava_get_auth():
    """Get connection parameters from config file

    Returns:
        str: client id
        str: client secret
        str: token
    """
    if os.path.exists(os.path.join(tempfile.gettempdir(), '.strava')):
        config = configparser.ConfigParser()
        config.read(os.path.join(tempfile.gettempdir(), '.strava'))
        if config.has_section('default'):
            if config.has_option('default', 'client_id') and \
                    config.has_option('default', 'client_secret') and \
                    config.has_option('default', 'token'):
                client_id = config.get('default', 'client_id', raw=False)
                client_secret = config.get('default', 'client_secret', raw=False)
                token = config.get('default', 'token', raw=False)
                return client_id, client_secret, token
            else:
                __logger__.error('Missing option in strava credentials. Please configure first')
                sys.exit(-1)
        else:
            __logger__.error('Missing section in Strava credentials. Please configure first')
            sys.exit(-1)
    else:
        __logger__.error('Missing Strava credentials cache file. Please configure first')
        sys.exit(-1)

