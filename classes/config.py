from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.backend import Backend
    from classes.repository import Repository
    from classes.schedule import Schedule
    from classes.job import Job


class Globals:
    restic_cache_dir: str
    restic_tmp_dir: str
    b2_account_id: str
    b2_account_key: str

class Config:
    config_path: str
    globals: Globals
    backends: dict[str, Backend]
    repositories: dict[str, Repository]
    schedules: dict[str, Schedule]
    jobs: dict[str, Job]
config : Config = Config()