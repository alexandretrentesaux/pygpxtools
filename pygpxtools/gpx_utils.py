# -*- encoding: utf-8 -*-

import os
import sys
import math
import datetime


def full_path(path):
    if path[0] == '~' and not os.path.exists(path):
        path = os.path.expanduser(path)
    return os.path.abspath(path)


def check_input_file(path, command):
    """Summary

    Args:
        path (TYPE): Description
    """
    if path is not None:
        extension = os.path.basename(path).split('.')[1]
        if extension != 'gpx':
            print('Error: not supported file extension {}'.format(extension))
            sys.exit(-1)
        return full_path(path)
    else:
        print('Error: --input is mandatory for pygpxtools_cli {}'.format(command))
        sys.exit(-1)


def check_output_file(path):
    if path is not None:
        extension = os.path.basename(path).split('.')[1]
        if extension != 'gpx':
            print('Error: not supported file extension {}'.format(extension))
            sys.exit(-1)
        return full_path(path)
    else:
        return '/home/alexantr/tmp/pygpxtools_' + datetime.datetime.today().strftime('%Y%m%d%H%M') + '.gpx'


def format_time(time_s, seconds=False):
    if not time_s:
        return 'n/a'
    elif seconds:
        return str(int(time_s))
    else:
        minutes = math.floor(time_s / 60.)
        hours = math.floor(minutes / 60.)
        return '{}:{}:{}'.format(str(int(hours)).zfill(2), str(int(minutes % 60)).zfill(2), str(int(time_s % 60)).zfill(2))