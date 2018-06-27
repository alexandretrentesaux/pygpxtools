# -*- encoding: utf-8 -*-

import os
import sys


def check_input_file(input):
    """Summary

    Args:
        input (TYPE): Description
    """
    if input is not None:
        extension = os.path.basename(input).split('.')[1]
        if extension != 'gpx':
            print('Error: not supported file extension {}'.format(extension))
            sys.exit(-1)
    else:
        print('Error: --input is mandatory for pygpxtools_cli cleanPause')
        sys.exit(-1)
