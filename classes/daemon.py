import re
import shutil
import threading
from time import sleep
from classes.config import config
from utils.utils import *

class daemon:
    def __init__(self) -> None:

        # Check for restic binary
        if not config.globals.restic_bin:
            logger.debug('Searching for restic binary')
            restic_binary = shutil.which('restic')
            config.globals.restic_bin = restic_binary
        else:
            restic_binary = config.globals.restic_bin

        if not restic_binary:
            logger.critical('No restic binary found in PATH')
            exit(1)

        restic_version = call([restic_binary, 'version'])['stdout'].decode().replace("\n", "")

        restic_version_regex = 'restic [\d\.]+ compiled with'

        if not re.match(restic_version_regex, restic_version):
            logger.critical(f'Invalid restic binary detected at path [{restic_binary}], version output was [{restic_version}]')
            exit(1)

        logger.info(f'Using [{restic_version}] located at [{restic_binary}]')

    def start(self):
        logger.info('Resticd started')

        while (True):
            for job_name in config.jobs:
                job = config.jobs[job_name]
                if job.is_time():
                    threading.Thread(target=job.backup).start()
            sleep(0.5)