#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import click
import os
import sys
import datetime
import pkg_resources
from clickclick import AliasedGroup
import gpxpy
import gpxpy.gpx


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

STYLES = {
    'FINE': {'fg': 'green'},
    'ERROR': {'fg': 'red'},
    'WARNING': {'fg': 'yellow', 'bold': True},
}

TITLES = {
    'state': 'Status',
    'creation_time': 'Creation Date',
    'id': 'Identifier',
    'desc': 'Description',
    'name': 'Name',
}

MAX_COLUMN_WIDTHS = {
    'desc': 50,
    'name': 20,
}


# Version
def print_version(ctx, param, value):
    """Summary

    Args:
        ctx (TYPE): Description
        param (TYPE): Description
        value (TYPE): Description

    Returns:
        TYPE: Description
    """
    if not value or ctx.resilient_parsing:
        return
    print('{}'.format(pkg_resources.require("pyoxeconf")[0]))
    click.echo('pygpxtools_cli version: {}'.format(__version__))
    ctx.exit()


def check_host_option(host):
    """Summary

    Args:
        host (TYPE): Description
    """
    if host is None:
        print('--host option is mandatory')
        exit(-1)


# CLI
@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.option('-V',
              '--version',
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True,
              help='Print the current version number and exit.')
def cli():
    """Summary
    """
    pass


@cli.command('cleanPause')
@click.option('--input', help='Input GPX file from Garmin Connect where remove pauses', default=None)
@click.option('--output', help='Output GPX file to upload to Strava', default=None)
def cli_clean_pause(input, output):
    """
    Clean pause in Garmin GPX file (currently support gpx file recorded with 1s between two track points.
    Only support files with .gpx extension.


    Args:
        input (STRING): filename or fullpath of GPX file to correct
        output (STRING): filename or fullpath for save corrected GPX

    Returns:
    """
    if input is not None:
        extension = os.path.basename(input).split('.')[1]
        if extension != 'gpx':
            print('Error: not supported file extension {}'.format(extension))
            sys.exit(-1)
        file = input
    else:
        print('Error: --input is mandatory for pygpxtools_cli cleanPause')
        sys.exit(-1)

    with open(file, 'r') as gpx_file:
        previous_time = None
        correction = 0
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if previous_time is None:
                        previous_time = point.time
                    else:
                        diff = point.time - previous_time
                        if diff.total_seconds() > 1:
                            correction += diff.total_seconds()
                    previous_time = point.time
                    if correction > 0:
                        point.time = point.time - datetime.timedelta(seconds=correction - 1)
        if output is None:
            output = '/home/alexantr/tmp/pygpxtools_' + datetime.datetime.today().strftime('%Y%m%d%H%M') + '.gpx'
        with open(output, 'w') as new_file:
            new_file.write(gpx.to_xml())


@cli.command('stravaUpload')
@click.option('--input', help='Input GPX file to upload to Strava', default=None)
@click.option('--login', help='Strava login', default=None)
@click.option('--password', help='Strava password', default=None)
def cli_strava_upload(input, login, password):
    print('todo')
