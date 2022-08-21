from classes.logger import logger

class Backend:
    name: str
    type: str

    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

class B2Backend(Backend):
    bucket: str
    account_id: str
    account_key: str

    def __init__(self, name: str, bucket: str, account_id: str, account_key: str) -> Backend:
        logger.debug(f'Creating B2 backend {name} with bucket {bucket}, account ID {account_id}, and account key {account_key}')
        super().__init__(name, 'b2')
        self.bucket = bucket
        self.account_id = account_id
        self.account_key = account_key

class FSBackend(Backend):
    path: str

    def __init__(self, name: str, path: str) -> Backend:
        logger.debug(f'Creating filesystem backend {name} with path {path}')
        super().__init__(name, 'filesystem')
        self.path = path