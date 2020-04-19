#!/usr/bin/env python

from utils import (lustre_quota_info, find_cache_dir)
import os, string
import shutil

import logging
logger = logging.getLogger(__name__)
### logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')

def cleanup_old_jobs(work_path, userid, volume_root, threshold=10.):
    """If free disk space is below percent threshold, start cleaning out old jobs."""

    percent_free = lustre_quota_info(userid, volume_root)

    if percent_free <= threshold:
        logger.info("Searching for old job dirs under %s to clean out to %02.2f%% free disk space." % (work_path, threshold))
        for root, dirs, files in os.walk(work_path, followlinks=True):
            dirs.sort()
            if '.done' not in files:
                continue
            logger.info("Cleaning out old job dir %s" % root)
            shutil.rmtree(root, ignore_errors=True)

            percent_free = lustre_quota_info(userid, volume_root)
            logger.info("percent_free: %s, threshold: %s" % (percent_free, threshold))
            if percent_free <= threshold:
                continue
            logger.info("Successfully freed up disk space to %02.2f%%." % percent_free)
            format("Successfully freed up disk space to %02.2f%%." % percent_free)
            return percent_free
        if percent_free <= threshold:
            logger.info("Failed to free up disk space to %02.2f%%." % threshold)
            print ("Failed to free up disk space to %02.2f%%." % threshold)
    return percent_free


def evict_localize_cache(work_path, userid, volume_root, threshold=10.):
    """If free disk space is below percent threshold, start evicting cache directories."""

    percent_free = lustre_quota_info(userid, volume_root)

    if percent_free <= threshold:
        logger.info("Evicting cached dirs under %s to clean out to %02.2f%% free disk space." % (work_path, threshold))
        for timestamp, signal_file, cache_dir in find_cache_dir(work_path):
            logger.info("Cleaning out cache dir %s" % cache_dir)
            shutil.rmtree(cache_dir, ignore_errors=True)

            percent_free = lustre_quota_info(userid, volume_root)
            logger.info("percent_free: %s, threshold: %s" % (percent_free, threshold))
            if percent_free <= threshold:
                continue
            logger.info("Successfully freed up disk space to %02.2f%%." % percent_free)
            return percent_free
        if percent_free <= threshold:
            logger.info("Failed to free up disk space to %02.2f%%." % threshold)
    return percent_free


def show_usage():
    print('Usage:\n')
    print('lustre_disk_cleanup.py --work_dir="/nobackupp12/lpan/worker/workdir/" --threshold=10.0 \n' )


import sys, getopt

def main(argv):

  # default values
  threshold = 10.0
  work_path = '/nobackupp12/lpan/worker/workdir/'

  try:
      opts, args = getopt.getopt(argv,"hd:t:",["work_dir=","threshold="])
      logger.debug('opts: %s' % opts)
      logger.debug('args: %s' % args)
  except getopt.GetoptError:
      show_usage()
      sys.exit(2)
  for opt, arg in opts:
      if opt in ('-h', '--help'):
          show_usage()
          sys.exit()
      elif opt in ("-d", "--work_dir"):
          work_path = arg
      elif opt in ("-t", "--threshold"):
          threshold = arg

  # check if work_path is valid
  if not os.path.isdir(work_path) and not work_path.startswith('/nobackup'):
    logger.error('work_dir %s does not exist or is not /nobackup*.' % work_path)
    show_usage()
    sys.exit(2)

  # the work_path looks like '{volume_root}/{userid}/...', e.g., '/nobackupp12/lpan/worker/workdir/'
  volume_root = '/' + work_path.split('/')[1]
  userid = work_path.split('/')[2]

  logger.debug('volume_root: %s' % volume_root)
  logger.debug('work_path: %s' % work_path)
  logger.debug('userid: %s' % userid)
  logger.debug('threshold: %s' % threshold)

  while True:
    # cleanup done jobs if free disk space not met
    cleanup_old_jobs(work_path, userid, volume_root, float(threshold))

    # cleanup localized datasets/PGEs if free disk space not met
    evict_localize_cache(work_path, userid, volume_root, float(threshold))


if __name__ == '__main__':
  main(sys.argv[1:])


