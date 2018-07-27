#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import click
import datetime
import pkg_resources
from clickclick import AliasedGroup
import gpxpy
import gpxpy.gpx
from pygpxtools.json_utils import *
from pygpxtools.gpx_utils import *
from pygpxtools.strava_utils import *


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
    print('{}'.format(pkg_resources.require("pygpxtools")[0]))
    # click.echo('pygpxtools_cli version: {}'.format(__version__))
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
@click.option('--input', help='Input GPX file from Garmin Connect where remove pauses', required=True, default=None)
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
    input = check_input_file(input, 'cleanPause')
    output = check_output_file(output)

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
    input = check_input_file(input, 'changeTimestamps')
    output = check_output_file(output)

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

        # print('Debug #01: gpx time: {} - new time {} / {}'.format(gpx.time, new_time, delta))
        # print('Debug #02: offset year : {}'.format(gpx.time.year - year))
        # print('Debug #03: offset month : {}'.format(gpx.time.month - month))
        # print('Debug #04: offset day : {}'.format(gpx.time.day - day))
        # print('Debug #05: offset hour : {}'.format(gpx.time.hour - hour))
        # print('Debug #06: offset minute : {}'.format(gpx.time.minute - minute))
        # print('Debug #07: offset second : {}'.format(gpx.time.second - second))
        # print('Debug #08: test shift : current = {} / new = {}'.format(gpx.time, gpx.time + delta))

        gpx.time = new_time
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    # print('Debug #08: point: {}/{} : current {} - update {}'.format(point.latitude, point.longitude, point.time, point.time + delta))
                    point.time = point.time + delta
        with open(output, 'w') as new_file:
            new_file.write(gpx.to_xml())


@cli.command('slowDown')
@click.option('--input', help='Input GPX file from Garmin Connect where remove pauses', default=None)
@click.option('--output', help='Output GPX file to upload to Strava',
              default='/home/alexantr/tmp/pygpxtools_' + datetime.datetime.today().strftime('%Y%m%d%H%M') + '.gpx')
@click.option('--factor', help='Slow down inter point factor in milliseconds', default=100)
def cli_slow(input, output, factor):
    """
    Decrease speed in Garmin GPX file in adding factor to current timestamp.
    Only support files with .gpx extension.


    Args:
        input (STRING): filename or fullpath of GPX file to correct
        output (STRING): filename or fullpath for save corrected GPX
        factor (INT): factor in milliseconds to apply to current timestamps

    Returns:
    """
    input = check_input_file(input, 'slowDown')
    output = check_output_file(output)

    correction = factor
    with open(input, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    point.time = point.time + datetime.timedelta(milliseconds=correction)
                    correction += factor
        with open(output, 'w') as new_file:
            new_file.write(gpx.to_xml())


@cli.command('stravaUpload')
@click.option('--input', help='Input GPX file to upload to Strava', default=None)
@click.option('--login', help='Strava login', default=None)
@click.option('--password', help='Strava password', default=None)
def cli_strava_upload(input, login, password):
    # input = check_input_file(input, 'stravaUpload')
    input = '/home/alexantr/Workspace/pygpxtools/resources/activity_2778234104.gpx'  # remove for dev only

    activity_title = ''
    activity_types = None

    with open('etc/garmin/activity_types_fr.json') as json_file:
        activity_types = json.loads(json_file.read())

    with open(input, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            print('Debug: track type: {} - track time: {}'.format(track.type, gpx.time))

            for item in activity_types['dictionary']:
                if item['key'] == track.type:
                    activity_title += item['display'] + ' '

            if gpx.time.hour < 6:
                activity_title += 'la nuit'
            elif 6 <= gpx.time.hour < 12:
                activity_title += 'le matin'
            elif 12 <= gpx.time.hour < 14:
                activity_title += 'le midi'
            elif 14 <= gpx.time.hour < 19:
                activity_title += 'l\'aprés-midi'
            elif 19 <= gpx.time.hour:
                activity_title += 'le soir'

            print('Debug# generated title: {}'.format(activity_title))

        clientId, clientSecret, token = strava_get_auth()
        print('Debug# Strava credentials - Id: {} - Secret : {} - Token {}'.format(clientId, clientSecret, token))


@cli.command('weatherUpdate')
@click.option('--input', help='Input GPX file from Garmin Connect where remove pauses', default=None)
@click.option('--output', help='Output GPX file to upload to Strava', default=None)
@click.option('--login', help='AccuWeather login', default=None)
@click.option('--password', help='AccuWeather password', default=None)
def cli_weather_update(input, login, password):
    # input = check_input_file(input, 'weatherUpdate')
    # output = check_output_file(output)
    print('todo')


@cli.command('summarize')
@click.option('--input', help='Input GPX file from Garmin Connect where remove pauses', default=None)
def cli_summarize(input):
    # input = check_input_file(input, 'summarize')
    # output = check_output_file(output)
    print('todo')
