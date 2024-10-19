__author__ = 'InfSub'
__contact__ = 'ADmin@TkYD.ru'
__copyright__ = 'Copyright (C) 2024, [LegioNTeaM] InfSub'
__date__ = '2024/10/19'
__deprecated__ = False
__email__ = 'ADmin@TkYD.ru'
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '2.2.10'


from os.path import exists

from app.utils.utils import aio_open, getenv, logging


logger = logging.getLogger(__name__)


STATUS_FILE_PATH = getenv('STATUS_FILE_PATH')


async def update_server_status(hostname: str, log_file_path: bool) -> None:
    # Проверка существования файла и его создание, если он отсутствует
    if not exists(STATUS_FILE_PATH):
        # Создание пустого файла
        async with aio_open(STATUS_FILE_PATH, mode='w') as file:
            await file.write('')

    status_line = f"{hostname} - {'Available' if log_file_path else 'Unavailable'}\n"
    updated = False

    # Чтение текущих статусов
    async with aio_open(STATUS_FILE_PATH, mode='r') as file:
        lines = await file.readlines()

    # Обновление или добавление статуса
    async with aio_open(STATUS_FILE_PATH, mode='w') as file:
        for line in lines:
            if line.startswith(hostname):
                await file.write(status_line)
                updated = True
            else:
                await file.write(line)

        if not updated:
            await file.write(status_line)
