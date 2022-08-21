import threading
from classes.logger import logger
from classes.repository import Repository
from classes.schedule import Schedule
from utils.utils import restic_cmd
from cron_validator import CronScheduler

class Job:
    name: str
    path: str
    schedule: Schedule
    repository: Repository
    is_running: bool
    __scheduler__: CronScheduler

    def __init__(self, name, path, schedule, repository):
        logger.debug(f'Creating job {name} with path {path}, schedule {schedule.name}, and repository {repository.name}')
        self.name = name
        self.path = path
        self.schedule = schedule
        self.repository = repository
        self.is_running = False

        self.__scheduler__ = CronScheduler(schedule.timer)

    def backup(self):
        self.is_running = True
        logger.info(f'Starting backup for job {self.name}')
        output = restic_cmd(self.repository, 'backup', ['', self.path])
        logger.info(output['stdout'].decode())
        logger.info(f'Next runtime for job {self.name} is {self.__scheduler__.next_execution_time}')
        self.is_running = False

    def is_time(self) -> bool:
        logger.debug(f'Checking if it is time to start job {self.name}')
        if self.is_running:
            logger.debug(f'Job {self.name} is currently running')
            return False
        elif self.__scheduler__.time_for_execution():
            logger.debug(f'It is time to start job {self.name}')
            return True
        else:
            logger.debug(f'It is not time to start job {self.name}')
            return False
        
