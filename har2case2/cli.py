""" Convert HAR (HTTP Archive) to YAML/JSON testcase for HttpRunner.

Usage:
    # convert to JSON format testcase
    >>> har2case2 demo.har

    # convert to YAML format testcase
    >>> har2case2 demo.har -2y

"""

import argparse
import logging
import sys

from har2case2.__about__ import __description__, __version__
from har2case2.core import HarParser


def main():
    """ HAR converter: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")
    parser.add_argument(
        '--log-level', default='INFO',
        help="Specify logging level, default is INFO.")
    parser.add_argument('har_source_file', nargs='?',
        help="Specify HAR source file")
    parser.add_argument(
        '-2y', '--to-yml', '--to-yaml',
        dest='to_yaml', action='store_true',
        help="Convert to YAML format, if not specified, convert to JSON format by default.")
    parser.add_argument(
        '-fmt', '--format',
        dest='fmt_version', default='v2',
        help="Specify YAML/JSON testcase format version, v2 corresponds to HttpRunner 2.2.0+.")
    parser.add_argument(
        '--filter', help="Specify filter keyword, only url include filter string will be converted.")
    parser.add_argument(
        '--exclude',
        help="Specify exclude keyword, url that includes exclude string will be ignored, multiple keywords can be joined with '|'")
    parser.add_argument(
        '--filter-header', help="Specify filter keyword, only header include filter string will be converted.")
    parser.add_argument(
        '--exclude-method',
        help="Specify exclude keyword, method that includes exclude string will be ignored, multiple keywords can be joined with '|'")

    args = parser.parse_args()

    if args.version:
        print("{}".format(__version__))
        exit(0)

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)

    har_source_file = args.har_source_file
    if not har_source_file or not har_source_file.endswith(".har"):
        logging.error("HAR file not specified.")
        sys.exit(1)

    logging.info(args.filter)
    logging.info(args.exclude)
    logging.info(args.filter_header)
    logging.info(args.exclude_method)
    
    output_file_type = "YML" if args.to_yaml else "JSON"
    HarParser(
        har_source_file, args.filter, args.exclude, args.filter_header, args.exclude_method
    ).gen_testcase(output_file_type, args.fmt_version.lower())

    return 0