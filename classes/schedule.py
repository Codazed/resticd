from classes.logger import logger

class Schedule:
    name: str
    path: str
    timer: str

    def __init__(self, name, timer):
        logger.debug(f'Creating schedule {name} with timer {timer}')
        self.name = name
        self.timer = timer
