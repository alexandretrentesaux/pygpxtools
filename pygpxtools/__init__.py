#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pkg_resources
from pygpxtools.logs_utils import *

__version__ = pkg_resources.require("pygpxtools")[0].version

logger = initialize_logger()
