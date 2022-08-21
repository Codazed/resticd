from datetime import datetime
import json
import re
from classes.backend import Backend
from classes.logger import logger
from utils.utils import restic_cmd, restic_cmd_json
import dateutil.parser

class Snapshot:
    id: str
    creation_date: datetime
    hostname: str
    tags: list[str]
    paths: list[str]

    def __init__(self, snapshot_dict):
        self.id = snapshot_dict['short_id']
        self.creation_date = dateutil.parser.parse(snapshot_dict['time'])
        self.hostname = snapshot_dict['hostname']
        self.paths = snapshot_dict['paths']

class Repository:
    name: str
    backend: Backend
    path: str
    password: str
    retention: str

    def __init__(self, name: str, backend: Backend, path: str, password: str, retention: str):
        logger.debug(f'Creating repository {name} with backend {backend.name}, path {path}, password {password}, and retention {retention}')
        self.name = name
        self.backend = backend
        self.path = path
        self.password = password
        self.retention = retention

    # Check the repository, returns True if no errors are found
    def check(self) -> bool:
        logger.info(f'Checking repository {self.name}')
        results: str = restic_cmd(self, 'check')['stdout'].decode()
        if re.match('no errors were found', results):
            return True
        else:
            return False

    def is_locked(self):
        logger.info(f'Checking if repository {self.name} is locked')
        results: str = restic_cmd(self, 'check')['stderr'].decode()
        if 'repository is already locked' in results:
            logger.info(f'Repository {self.name} is locked')
            pid = re.search('PID \d+', results).group(0)
            hostname_by_user = re.search('on \w+ by \w+ \(UID \d+, GID \d+\)', results).group(0)
            hostname_user_info = hostname_by_user.split()
            return {
                'PID': pid.split()[1],
                'Hostname': hostname_user_info[1],
                'User': hostname_user_info[3],
                'UID': hostname_user_info[5].removesuffix(','),
                'GID': hostname_user_info[7].removesuffix(')')
            }
        else:
            logger.info(f'Repository {self.name} is not locked')
            return False

    async def snapshots(self) -> list[Snapshot]:
        logger.info(f'Getting snapshots for repository {self.name}')
        snapshots_json = json.loads(restic_cmd_json(self, 'snapshots')['stdout'].decode())
        snapshots = []
        for snapshot_json in snapshots_json:
            snapshots.append(Snapshot(snapshot_json))
        return snapshots

