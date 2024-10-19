__author__ = 'InfSub'
__contact__ = 'ADmin@TkYD.ru'
__copyright__ = 'Copyright (C) 2024, [LegioNTeaM] InfSub'
__date__ = '2024/10/19'
__deprecated__ = False
__email__ = 'ADmin@TkYD.ru'
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '2.2.10'


from asyncio import (
    run as aio_run, sleep as aio_sleep, create_task as aio_create_task, gather as aio_gather,
    get_event_loop as aio_get_event_loop
)
from aiofiles import open as aio_open
from typing import Dict as type_Dict, List as type_List, Optional as type_Optional, Union as type_Union
from pathlib import Path
from os import getenv
from os.path import join as os_join
from dotenv import load_dotenv
from pprint import pprint

from app.utils.logging_config import logging, setup_logging


# Загрузка переменных из .env файла
load_dotenv()


LOGGING_SILENCE_LIBRARY = getenv('LOGGING_SILENCE_LIBRARY').replace(' ', '').split(',')

setup_logging(list_silence_lib=LOGGING_SILENCE_LIBRARY)
# logger = logging.getLogger(__name__)


__all__ = [
    'aio_run', 'aio_sleep', 'aio_create_task', 'aio_gather', 'aio_get_event_loop',
    'aio_open',
    'type_Dict', 'type_List', 'type_Optional', 'type_Union',
    'getenv', 'os_join',
    'Path',
    'logging',
    'pprint'

]
