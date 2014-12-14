#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
regularize filenames
"""

import argparse
from functools import wraps
import logging
import os
import re
import shutil
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
    logger = logging.getLogger(sys._getframe().f_code.co_name)


    indir = os.path.abspath(args.indir)
    outdir = os.path.abspath(args.outdir)
    # test for existence of input directory
    if not(os.path.isdir(indir)):
        logger.critical ("normalized input directory path is not an existing directory: %s" % indir)
        sys.exit(1)

    if not(os.path.isdir(outdir)):
        logger.critical ("normalized output directory path is not an existing directory: %s" % outdir)
        sys.exit(1)

    logger.debug("normalized input file directory path is: '%s'" % indir)
    logger.debug("normalized output file directory path is: '%s'" % outdir)

    # get list of files and loop through them
    infiles = []
    for (dirpath, dirnames, filenames) in os.walk(indir):
        infiles.extend(filenames)
        break

    for fn in infiles:

        logger.debug("handling '%s'" % fn)

        # lower-case this name
        newfn = fn.lower()
        logger.debug("after conversion to lower case: '%s'" % newfn)

        # regularize whitespace and replace with hyphen
        newfn = re.sub(r'\s+', '-', newfn.strip())
        logger.debug("after whitespace normalization and hyphen substitution: '%s'" % newfn)

        # replace all punctuation except hyphens and underlines with hyphens (preserve extension)
        n, ext = os.path.splitext(newfn)
        words = re.split(r'\W+', n)
        n = '-'.join(words)
        newfn = ''.join((n, ext))
        logger.debug("normalized punctuation: '%s'" % newfn)

        # clean up multiple hyphens
        newfn = re.sub(r'\-+', '-', newfn)
        logger.debug("after hyphen normalization: '%s'" % newfn)

        # copy the file contents to the newly named file in the output directory
        src = os.path.join(indir, fn)
        dst = os.path.join(outdir, newfn)
        shutil.copyfile(src, dst)

        # write change notice to logger
        logger.info("wrote '%s' to '%s'" % (fn, newfn))


if __name__ == "__main__":
    log_level = DEFAULTLOGLEVEL
    log_level_name = logging.getLevelName(log_level)
    logging.basicConfig(level=log_level)

    try:
        parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument ("-l", "--loglevel", type=str, help="desired logging level (case-insensitive string: DEBUG, INFO, WARNING, ERROR" )
        parser.add_argument ("-v", "--verbose", action="store_true", default=False, help="verbose output (logging level == INFO")
        parser.add_argument ("-vv", "--veryverbose", action="store_true", default=False, help="very verbose output (logging level == DEBUG")
        parser.add_argument ("indir", help="input directory path")
        parser.add_argument ("outdir", help="output directory path")
        # example positional argument:
        # parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
        args = parser.parse_args()
        if args.loglevel is not None:
            args_log_level = re.sub('\s+', '', args.loglevel.strip().upper())
            try:
                log_level = getattr(logging, args_log_level)
            except AttributeError:
                logging.error("command line option to set log_level failed because '%s' is not a valid level name; using %s" % (args_log_level, log_level_name))
        if args.veryverbose:
            log_level = logging.DEBUG
        elif args.verbose:
            log_level = logging.INFO
        log_level_name = logging.getLevelName(log_level)
        logging.getLogger().setLevel(log_level)
        if log_level != DEFAULTLOGLEVEL:
            logging.warning("logging level changed to %s via command line option" % log_level_name)
        else:
            logging.info("using default logging level: %s" % log_level_name)
        logging.debug("command line: '%s'" % ' '.join(sys.argv))
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
