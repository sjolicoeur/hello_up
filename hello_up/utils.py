import json
import random
import os
import subprocess
import tempfile
# import the logging library
import logging
from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# print(BASE_DIR)

# with open(os.path.join(BASE_DIR, 'dictionary.json')) as f:
#     dictionary = json.loads(f.read())


def unsafe_execute_command(cmd_array):
    env = {
        "IDEAL_PATH": "/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin",
        "PATH": os.getenv("PATH", ""),
        "DO_API_TOKEN": os.getenv("DO_API_TOKEN", ""),
    }
    start = datetime.now()
    try:
        result = subprocess.check_output(
            cmd_array, shell=True, universal_newlines=True,
            stderr=subprocess.STDOUT, env=env)  # .decode('ascii').strip()
        end = datetime.now() - start
        logger.error("it took %s seconds for: %s" % (end.total_seconds(), cmd_array))
        return result
    except subprocess.CalledProcessError as e:
        end = datetime.now() - start
        logger.error('Something went wrong! %s seconds' % end.total_seconds())
        logger.error("ERRROR", e.output)
        # logger.debug ("ERRROR", e.output)
        raise e

