#!/usr/bin/env python

from utils import find_cache_dir
from utils import lustre_quota_info
import os, string, time
import shutil
import sys, getopt


#----------------------------------------------------------------------

# check every this many seconds
check_interval = 600

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')

def cleanup_old_jobs(work_path, userid, volume_root, threshold=10.):
    """If free disk space is below percent threshold, start cleaning out old jobs."""

    percent_free = lustre_quota_info(userid, volume_root)
    logger.debug('percent_free: %s' % str(percent_free))

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
    else:
        logger.info("No need to free up disk space; not yet filled up to %02.2f%%." % threshold)

    return percent_free


def evict_localize_cache(work_path, userid, volume_root, threshold=10.):
    """If free disk space is below percent threshold, start evicting cache directories."""

    percent_free = lustre_quota_info(userid, volume_root)
    logger.debug('percent_free: %s' % str(percent_free))

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
    else:
        logger.info("No need to free up disk space; not yet filled up to %02.2f%%." % threshold)

    return percent_free



def remove(path):
    """
    Remove the file or directory
    """
    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except OSError:
            logger.info("Unable to remove folder: %s" % path)
    else:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            logger.info("Unable to remove file: %s" % path)




def cleanup(number_of_days, path):
    """
    Removes files from the passed in path that are older than or equal 
    to the number_of_days
    """
    time_in_secs = time.time() - (number_of_days * 24 * 60 * 60)
    for root, dirs, files in os.walk(path, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            ### logger.info('full_path: %s' % full_path)
            try:
              stat = os.stat(full_path)
              if stat.st_mtime >= time_in_secs:
                  remove(full_path)
                  logger.info('removed file: %s' % full_path)
            except FileNotFoundError:
              islink = os.path.islink(full_path)
              if islink:
                os.unlink(full_path)
                logger.info('unlinked full_path: %s' % full_path)

        if not os.listdir(root):
            remove(root)
            logger.info('removed dir: %s' % root)



def show_usage():
    print('Usage:\n')
    print('lustre_disk_cleanup.py --work_dir="/nobackupp12/lpan/worker/workdir/" --threshold=10.0 \n' )


def main(argv):

  # default values
  threshold = 10.0
  threshold_dt = 5.0
  days = 21
  ### work_path = '/nobackupp12/lpan/worker/workdir/'
  work_path = '/nobackupp12/lpan/worker/'

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
  if not os.path.isdir(work_path) or not work_path.startswith('/nobackup'):
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
    # cleanup old files that are days old
    cleanup(days, work_path)

    # cleanup done jobs if free disk space not met
    cleanup_old_jobs(work_path, userid, volume_root, float(threshold))

    # cleanup localized datasets/PGEs if free disk space not met
    evict_localize_cache(work_path, userid, volume_root, float(threshold)+threshold_dt)

    time.sleep(check_interval)


if __name__ == '__main__':
  main(sys.argv[1:])


