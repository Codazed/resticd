from __future__ import annotations
import os
import subprocess
from classes.logger import logger
from classes.config import config

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.repository import Repository

def call(command: list[str], env=os.environ) -> dict:
        logger.debug(f'Invoking {command}')
        results = subprocess.run(command, capture_output=True, env=env)
        return {
            'return_code': results.returncode,
            'stdout': results.stdout,
            'stderr': results.stderr
        }

def restic_cmd(repository: Repository, command: str, args=[]):
        logger.debug(f'Running restic command {command} for repository {repository.name}')
        env = {}
        if repository.backend.type == 'b2':
            restic_repo = f'b2:{repository.backend.bucket}:{repository.path}'
            
            # Set b2 env
            env['B2_ACCOUNT_ID'] = repository.backend.account_id
            env['B2_ACCOUNT_KEY'] = repository.backend.account_key

        env['RESTIC_CACHE_DIR'] = config.globals.restic_cache_dir
        env['TMPDIR'] = config.globals.restic_tmp_dir

        env['RESTIC_REPOSITORY'] = restic_repo
        env['RESTIC_PASSWORD'] = repository.password
            
        return call([config.globals.restic_bin, command] + args, env)

def restic_cmd_json(repository: Repository, command: str, args=[]):
    args.append('--json')
    return restic_cmd(repository, command, args)