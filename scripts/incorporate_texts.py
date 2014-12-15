#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run a series of EpiDoc edition div incorporation transforms
"""

import argparse
import csv
from functools import wraps
import hashlib
import logging
import os
import re
import subprocess
import sys
import traceback

DEFAULTLOGLEVEL = logging.WARNING

def arglogger(func):
    """
    decorator to log argument calls to functions
    """
    @wraps(func)
    def inner(*args, **kwargs): 
        logger = logging.getLogger(func.__name__)
        logger.debug("called with arguments: %s, %s" % (args, kwargs))
        return func(*args, **kwargs) 
    return inner    




@arglogger
def main (args):
    """
    main functions
    """

    # set up logging
    logger = logging.getLogger()
    log_level = DEFAULTLOGLEVEL
    if args.loglevel is not None:
        args_log_level = re.sub('\s+', '', args.loglevel.strip().upper())
        try:
            log_level = getattr(logger, args_log_level)
        except AttributeError:
            logger.error("command line option to set log_level failed because '%s' is not a valid level name; using %s" % (args_log_level, log_level_name))
    elif args.veryverbose:
        log_level = logging.DEBUG
    elif args.verbose:
        log_level = logging.INFO
    log_level_name = logging.getLevelName(log_level)
    logger.setLevel(log_level)
    if log_level != DEFAULTLOGLEVEL:
        logger.warning("logging level changed to %s via command line option" % log_level_name)
    else:
        logger.info("using default logging level: %s" % log_level_name)
    logger.debug("command line: '%s'" % ' '.join(sys.argv))

    # iterate through list of candidate TM numbers
    manifest = open(args.candidates, 'r')
    candidates = [c.strip() for c in manifest]
    manifest.close()
    for candidate in candidates:
        logger.debug("candidate: '%s'" % candidate)

        # determine paths to related files
        metaf = os.path.join((args.metadir, str(int(candidate[0:1]+1)), "%s.xml" % candidate))
        editionf = os.path.join((args.editiondir, "%s.xml" % candidate))

        if os.name == 'posix':
        #    cmd = ['saxon', '-xsl:%s' % xslt_file_path, '-o:%s' % output_file_path, '-s:%s' % candidate_file_path, 'collection="%s"' % candidate_collection, 'analytics="no"', 'cssbase="/css"', 'jsbase="/js"' ]
        #    logger.debug(' '.join(cmd))
        #    subprocess.call(' '.join(cmd), shell=True)       
            pass
        else:
            # handle it on pc
            pass


if __name__ == "__main__":
    log_level = DEFAULTLOGLEVEL
    log_level_name = logging.getLevelName(log_level)
    logging.basicConfig(level=log_level)

    try:
        parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument ("-l", "--loglevel", type=str, help="desired logging level (case-insensitive string: DEBUG, INFO, WARNING, ERROR" )
        parser.add_argument ("-v", "--verbose", action="store_true", default=False, help="verbose output (logging level == INFO")
        parser.add_argument ("-vv", "--veryverbose", action="store_true", default=False, help="very verbose output (logging level == DEBUG")
        parser.add_argument ("-c", "--candidates", required=True, help="path to text file containing a list of TM numbers to try to operate on")
        parser.add_argument ("-m", "--metadir", required=True, help="path to directory containing metadata XML files")
        parser.add_argument ("-e", "--editiondir", required=True, help="path to directory containing edition division files")
        # example positional argument:
        # parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
        args = parser.parse_args()
        main(args)
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print "ERROR, UNEXPECTED EXCEPTION"
        print str(e)
        traceback.print_exc()
        os._exit(1)
