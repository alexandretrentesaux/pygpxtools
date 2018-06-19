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
    Clean pause in Garmin GPX file (currently support gpx file recorded with 1s offset between two track points
    (doesn't work with intelligent data recording). Only support files with .gpx extension.


    Args:
        input (STRING): filename or fullpath of GPX file to correct
        output (STRING): filename or fullpath for save corrected GPX

    Returns:
    """
    check_input_file(input)

    with open(input, 'r') as gpx_file:
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


@cli.command('changeTimestamps')
@click.option('--input', help='Input GPX file from Garmin Connect where remove pauses', default=None)
@click.option('--output', help='Output GPX file to upload to Strava', default=None)
@click.option('--year', help='year to update timestamps', type=int, default=None)
@click.option('--month', help='month to update timestamps', type=int, default=None)
@click.option('--day', help='day to update timestamps', type=int, default=None)
@click.option('--hour', help='hour to update timestamps', type=int, default=None)
@click.option('--minute', help='minute to update timestamps', type=int, default=None)
@click.option('--second', help='second to update timestamps', type=int, default=None)
def cli_change_timestamps(input, output, year, month, day, hour, minute, second):
    """
    Change time stamps in GPX file

    Args:
        input (STRING): filename or fullpath of GPX file to correct
        output (STRING): filename or fullpath for save corrected GPX
        year (INT): year to apply to timestamps
        month (INT): month to apply to timestamps
        day (INT): day to apply to timestamps
        hour (INT): hour to apply to timestamps
        minute (INT): minute to apply to timestamps
        second (INT): second to apply to timestamps

    Returns:
    """
    check_input_file(input)

    with open(input, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        if year is None:
            year = gpx.time.year
        if month is None:
            month = gpx.time.month
        if day is None:
            day = gpx.time.day
        if hour is None:
            hour = gpx.time.hour
        if minute is None:
            minute = gpx.time.minute
        if second is None:
            second = gpx.time.second

        new_time = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        delta = new_time - gpx.time

        # print('Debug #01: gpx time: {} - new time {} - {}'.format(gpx.time, new_time, delta.days))
        # print('Debug #02: offset year : {}'.format(gpx.time.year - year))
        # print('Debug #03: offset month : {}'.format(gpx.time.month - month))
        # print('Debug #04: offset day : {}'.format(gpx.time.day - day))
        # print('Debug #05: offset hour : {}'.format(gpx.time.hour - hour))
        # print('Debug #06: offset minute : {}'.format(gpx.time.minute - minute))
        # print('Debug #07: offset second : {}'.format(gpx.time.second - second))

        gpx.time = new_time
        # first = None
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    point.time = point.time + delta
                    # if first is None:  # debug print 1st point for debug
                    #     print('Debug #08: point: {}/{} : {}'.format(point.latitude, point.longitude, point.time))
                    #     first = point.time
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


@cli.command('weatherUpdate')
@click.option('--input', help='Input GPX file from Garmin Connect where remove pauses', default=None)
@click.option('--output', help='Output GPX file to upload to Strava', default=None)
@click.option('--login', help='AccuWeather login', default=None)
@click.option('--password', help='AccuWeather password', default=None)
def cli_weather_update(input, login, password):
    print('todo')


@cli_command('summarize')
@click.option('--input', help='Input GPX file from Garmin Connect where remove pauses', default=None)
def cli_summarize(input):
    print('todo')

