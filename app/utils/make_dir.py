__author__ = 'InfSub'
__contact__ = 'ADmin@TkYD.ru'
__copyright__ = 'Copyright (C) 2024, [LegioNTeaM] InfSub'
__date__ = '2024/09/29'
__deprecated__ = False
__email__ = 'ADmin@TkYD.ru'
__maintainer__ = 'InfSub'
__status__ = 'Production'
__version__ = '2.0.4'


from aiofiles.os import makedirs
from app.utils.utils import Path, logging


logger = logging.getLogger(__name__)


async def make_dir(directory: str) -> None:
    """Проверяет наличие каталога и создает его при необходимости."""
    path = Path(directory)
    try:
        await makedirs(path, exist_ok=True)
        logger.info(f'Directory {directory} created successfully.')
    except Exception as e:
        logger.error(f'An error occurred: {e}')

