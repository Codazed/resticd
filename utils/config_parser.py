import os
import yaml

from classes.logger import logger
from classes.backend import *
from classes.repository import Repository
from classes.schedule import Schedule
from classes.job import Job
from classes.config import Config, Globals

def parse_config(config_path: str, d: Config):

    config_full_path = os.path.abspath(config_path)
    logger.debug(f'Creating new config object from path {config_full_path}')
    d.config_path = config_full_path

    # Parse config file
    with open(config_full_path, 'r') as stream:
        for data in yaml.safe_load_all(stream):
            parsed_config = data

    # Get global config
    global_config = parsed_config['global']
    if global_config:
        d.globals = Globals()
        d.globals.restic_bin = global_config['restic_bin'] if 'restic_bin' in global_config else None
        d.globals.restic_cache_dir = global_config['restic_cache_dir'] if 'restic_cache_dir' in global_config else None
        d.globals.restic_tmp_dir = global_config['restic_tmp_dir'] if 'restic_tmp_dir' in global_config else None
        d.globals.b2_account_id = global_config['b2_account_id'] if 'b2_account_id' in global_config else None
        d.globals.b2_account_key = global_config['b2_account_key'] if 'b2_account_key' in global_config else None
    
    # Get backends
    d.backends = {}
    logger.info('Parsing backends')

    if not 'backends' in parsed_config:
        logger.error('No backends defined')
        exit(1)

    backends = parsed_config['backends']

    for backend_name in backends:
        backend = backends[backend_name]

        # Backblaze B2 backends
        if backend['type'] == 'b2':

            # Get account ID
            account_id: str
            if 'account_id' in backend:
                account_id = backend['account_id']
            elif d.globals.b2_account_id:
                account_id = d.globals.b2_account_id
            else:
                logger.error(f'No B2 account ID specified for backend {backend_name}')
                exit(1)
            
            # Get account key
            account_key: str
            if 'account_key' in backend:
                account_key = backend['account_key']
            elif d.globals.b2_account_key:
                account_key = d.globals.b2_account_key
            else:
                logger.error(f'No B2 account key specified for backend {backend_name}')
                exit(1)

            d.backends[backend_name] = B2Backend(
                backend_name,
                backend['bucket'],
                account_id,
                account_key
            )

        # Filesystem backends
        elif backend['type'] == 'filesystem':
            d.backends[backend_name] = FSBackend(
                backend_name,
                backend['path']
            )

    # Get repositories
    d.repositories = {}
    logger.info('Parsing repositories')

    if not 'repositories' in parsed_config:
        logger.warn('No repositories defined')
        repositories = []
    else:
        repositories = parsed_config['repositories']
    
    for repository_name in repositories:
        repository = repositories[repository_name]

        # Get the backend for the repo
        if not repository['backend'] in d.backends:
            logger.error(f'No backend {repository["backend"]} found for repository {repository_name}')
            exit(1)
        
        backend = d.backends[repository['backend']]

        d.repositories[repository_name] = Repository(
            repository_name,
            backend,
            repository['path'],
            repository['password'],
            repository['retention_policy']
        )

    # Get schedules
    d.schedules = {}
    logger.info('Parsing schedules')

    if not 'schedules' in parsed_config:
        logger.warn('No schedules defined')
        schedules = []
    else:
        schedules = parsed_config['schedules']

    for schedule_name in schedules:
        schedule = schedules[schedule_name]

        d.schedules[schedule_name] = Schedule(
            schedule_name,
            schedule
        )

    # Get jobs
    d.jobs = {}
    logger.info('Parsing jobs')

    if not 'jobs' in parsed_config:
        logger.warn('No jobs defined')
        jobs = []
    else:
        jobs = parsed_config['jobs']

    for job_name in jobs:
        job = jobs[job_name]

        # Get the schedule for the repo
        if not job['schedule'] in d.schedules:
            logger.error(f'No schedule {job["schedule"]} found for job {job_name}')
            exit(1)
        
        schedule = d.schedules[job['schedule']]

        # Get the repo for the job
        if not job['repository'] in d.repositories:
            logger.error(f'No repository {job["repository"]} found for job {job_name}')
            exit(1)
        
        repository = d.repositories[job['repository']]

        d.jobs[job_name] = Job(
            job_name,
            job['path'],
            schedule,
            repository
        )
        
    logger.info(f'Finished loading config from file {config_full_path}')