#!/usr/bin/env python
"""
HySDS inactivity daemon to perform scale down of auto scaling group/spot fleet
request and perform self-termination (harikiri) of the instance. If a keep-alive 
signal file exists at <root_work_dir>/.harikiri, then self-termination is bypassed
until it is removed.
"""
from builtins import str
from future import standard_library
standard_library.install_aliases()
import os
import signal
import sys
import time
import re
import json
import socket
import requests
import logging
import argparse
import traceback
import backoff
from random import randint
from subprocess import call
from datetime import datetime
from pprint import pformat


log_format = "[%(asctime)s: %(levelname)s/%(funcName)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)


DAY_DIR_RE = re.compile(r'jobs/\d{4}/\d{2}/\d{2}/\d{2}/\d{2}$')

NO_JOBS_TIMER = None

KEEP_ALIVE = False


def log_event(url, event_type, event_status, event, tags):
    """Log custom event."""

    params = {
        'type': event_type,
        'status': event_status,
        'event': event,
        'tags': tags,
        'hostname': socket.getfqdn(),
    }
    headers = {'Content-type': 'application/json'}
    r = requests.post("%s/event/add" % url, data=json.dumps(params),
                      verify=False, headers=headers)
    r.raise_for_status()
    resp = r.json()
    return resp


def keep_alive(root_work):
    """Check if the keep alive signal exists."""

    return True if os.path.exists(os.path.join(root_work, ".harikiri")) else False


def is_jobless(root_work, inactivity_secs, logger=None):
    """Check if no jobs are running and hasn't run in the past 
       amount of time passed in.
    """

    global NO_JOBS_TIMER
    global KEEP_ALIVE

    # check if keep-alive
    logging.info("KEEP_ALIVE: %s" % KEEP_ALIVE)
    if keep_alive(root_work):
        ### logging.info("keep_alive(root_work) is True")
        if KEEP_ALIVE != True:
            KEEP_ALIVE = True
            if logger is not None:
                try:
                    print((log_event(logger, 'harikiri', 'keep_alive_set', {}, [])))
                except:
                    pass
        logging.info("Keep-alive exists.")
        return
    else:
        ### logging.info("keep_alive(root_work) is False")
        if KEEP_ALIVE != False:
            KEEP_ALIVE = False
            if logger is not None:
                try:
                    print((log_event(logger, 'harikiri', 'keep_alive_unset', {}, [])))
                except:
                    pass
            logging.info("Keep-alive removed.")

    most_recent = None
    for root, dirs, files in os.walk(root_work, followlinks=True):
        match = DAY_DIR_RE.search(root)
        if not match:
            continue
        dirs.sort()
        for d in dirs:
            job_dir = os.path.join(root, d)
            done_file = os.path.join(job_dir, '.done')
            if not os.path.exists(done_file):
                logging.info(
                    "%s: no .done file found. Not jobless yet." % job_dir)
                return False
            t = os.path.getmtime(done_file)
            done_dt = datetime.fromtimestamp(t)
            age = (datetime.utcnow() - done_dt).total_seconds()
            if most_recent is None or age < most_recent:
                most_recent = age
            logging.info("%s: age=%s" % (job_dir, age))
    if most_recent is None:
        if NO_JOBS_TIMER is None:
            NO_JOBS_TIMER = time.time()
        else:
            if (time.time() - NO_JOBS_TIMER) > inactivity_secs:
                return True
        return False
    if most_recent > inactivity_secs:
        return True
    return False


def seppuku(pid, logger=None):
    """Shutdown supervisord and the instance if it detects that it is 
       currently part of an autoscale group."""

    logging.info("Initiating seppuku.")

    # gracefully shutdown
    try:
        graceful_shutdown(pid, logger)
    except Exception as e:
        logging.error("Got exception in graceful_shutdown(): %s\n%s" %
                      (str(e), traceback.format_exc()))


def graceful_shutdown(pid, logger=None):
    """Gracefully shutdown by sigterm kill the celery process
       and shutdown."""

    # detach and die
    logging.info("Committing seppuku.")

    # log seppuku
    if logger is not None:
        try:
            logging.info(log_event(logger, 'harikiri', 'shutdown', {}, []))
        except:
            pass

    # kill celery process
    print ('killing pid: ', pid)
    try:
      os.kill(pid, signal.SIGTERM)
      ### sys.exit(0)
    except ProcessLookupError:
      logging.info('Process %s already ended.'%str(pid))
      ### sys.exit(0)


def harikiri(root_work, inactivity_secs, check_interval, pid, logger=None):
    """If no jobs are running and the last job finished more than the 
       threshold, shutdown supervisord gracefully then shutdown the 
       instance.
    """

    """
    logging.info("harikiri configuration:")
    logging.info("root_work_dir=%s" % root_work)
    logging.info("inactivity=%d" % inactivity_secs)
    logging.info("check=%d" % check_interval)
    logging.info("logger=%s" % logger)

    print ('pid: ', pid)
    """

    while True:
        if is_jobless(root_work, inactivity_secs, logger):
            logging.info("is_jobless() returns True.")
            try:
                seppuku(pid, logger)
            except Exception as e:
                logging.error("Got exception in seppuku(): %s\n%s" %
                              (str(e), traceback.format_exc()))
        time.sleep(check_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root_work_dir',
                        help="root HySDS work directory, e.g. /data/work")
    parser.add_argument('-i', '--inactivity', type=int, default=600,
                        help="inactivity threshold in seconds")
    parser.add_argument('-c', '--check', type=int, default=60,
                        help="check for inactivity every N seconds")
    parser.add_argument('-p', '--pid', type=int, default=0,
                        help="PID of celery job worker process")
    parser.add_argument('-l', '--logger', type=str, default=None,
                        help="enable event logging; specify Mozart REST API," +
                              " e.g. https://192.168.0.1/mozart/api/v0.1")
    args = parser.parse_args()

    harikiri(args.root_work_dir, args.inactivity, args.check, args.pid, args.logger)
