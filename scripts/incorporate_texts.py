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

XSLT_FILE_NAME = 'insert-edition.xsl'


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

    # make sure output directory is valid
    outputdir = os.path.abspath(args.outputdir)
    if not(os.path.isdir(outputdir)):
        raise IOError("'%s' is not a directory" % outputdir)

    # make sure we know where to get the stylesheet
    script_path = os.path.realpath(__file__)
    logger.debug("script path is '%s'" % script_path)
    script_dir, script_name = os.path.split(script_path)
    logger.debug("script dir is '%s'" % script_dir)
    xslt_file_path = os.path.abspath(os.path.join(script_dir, '..', XSLT_FILE_NAME))    
    if not(os.path.isfile(xslt_file_path)):
        raise IOError("cannot find XSLT file at '%s'" % xslt_file_path)

    # iterate through list of candidate TM numbers
    manifest = open(args.candidates, 'r')
    candidates = [c.strip() for c in manifest]
    manifest.close()
    for candidate in candidates:
        logger.debug("candidate: '%s'" % candidate)

        # determine paths to related files
        metaf = os.path.abspath(os.path.join(args.metadir, str(int(candidate[0:2])+1), "%s.xml" % candidate))
        editionf = os.path.abspath(os.path.join(args.editiondir, "%s.xml" % candidate))
        logger.debug("metaf: '%s'" % metaf)
        logger.debug("editionf: '%s'" % editionf)
        if not(os.path.isfile(metaf)):
            logger.error("failed to find metadata file at '%s'" % metaf)
        elif not(os.path.isfile(editionf)):
            logger.error("failed to find edition file at '%s'" % editionf)
        else:
            editiondir, editionname = os.path.split(editionf)
            outf = os.path.abspath(os.path.join(outputdir, "%s.xml" % candidate))
            logger.debug("outf: '%s'" % outf)            
            if os.name == 'posix':
                cmd = ['saxon', '-xsl:%s' % xslt_file_path, '-o:%s' % outf, '-s:%s' % metaf, 'who="%s"' % args.who, 'input-directory="%s"' % editiondir]
                logger.debug(' '.join(cmd))
                subprocess.call(' '.join(cmd), shell=True)     
            else:
                # handle it on pc
                logger.critical("this script does not have support for Windows!")
                os.exit(1)


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
        parser.add_argument ("-o", "--outputdir", required=True, help="path to directory in which to output results")
        parser.add_argument ("-w", "--who", required=True, help="Name of person to be credited in the revision description for running this script")
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
