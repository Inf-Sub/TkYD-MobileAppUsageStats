__author__ = 'InfSub'
__contact__ = 'ADmin@TkYD.ru'
__copyright__ = 'Copyright (C) 2024, [LegioNTeaM] InfSub'
__date__ = '2024/10/19'
__deprecated__ = False
__email__ = 'ADmin@TkYD.ru'
__maintainer__ = 'InfSub'
__status__ = 'Development'  # 'Production / Development'
__version__ = '2.2.10'


from time import time
from datetime import datetime as dt

from app.utils.utils import aio_run, aio_sleep, aio_gather, aio_create_task, Path, os_join, getenv, logging, pprint
from app.parse.convert_sma_log_data_to_dict import log_parser
from app.config import REPO_DIR, DATA_DIR
from app.smb.smb_files import run as smb_run
from app.utils.convert_charset import convert_to_utf8
from app.utils.server_status import update_server_status


logger = logging.getLogger(__name__)


SHOPS = getenv('SHOPS').replace(' ', '').split(',')

SMB_HOSTNAME_TEMPLATE = getenv('SMB_HOSTNAME_TEMPLATE')
SMB_SHARE = getenv('SMB_SHARE')
SMB_PATH = getenv('SMB_PATH')
SMB_USERNAME = getenv('SMB_USERNAME')
SMB_PASSWORD = getenv('SMB_PASSWORD')

LOAD_TO_PATH = os_join(REPO_DIR, getenv('LOAD_TO_PATH'))
LOAD_FILE_PATTERN = getenv('LOAD_FILE_PATTERN')
SMB_SLEEP_INTERVAL = int(getenv('SMB_SLEEP_INTERVAL'))

DB_HOST = getenv('DB_HOST')
DB_PORT = int(getenv('DB_PORT'))
DB_NAME = getenv('DB_NAME')
DB_USERNAME = getenv('DB_USERNAME')
DB_PASSWORD = getenv('DB_PASSWORD')

# DB_INIT_DATA_CITIES_PATH = os_join(DATA_DIR, getenv('DB_INIT_DATA_CITIES_FILE_PATH'))
# DB_INIT_DATA_STORES_PATH = os_join(DATA_DIR, getenv('DB_INIT_DATA_STORES_FILE_PATH'))
DB_INIT_SCHEMAS = getenv('DB_INIT_SCHEMAS')


async def ln(num: int = 30) -> str:
    return f'\n{"=" * num}'


async def perform_smb_task(shop_id: str) -> None:
    hostname = SMB_HOSTNAME_TEMPLATE.format(shop_id)
    start_connect_time = time()

    try:
        log_file_path = await smb_run(
            server=hostname, share=SMB_SHARE, path=SMB_PATH, username=SMB_USERNAME, password=SMB_PASSWORD,
            file_pattern=LOAD_FILE_PATTERN, download_path=LOAD_TO_PATH, download_file_name=shop_id
        )

        logger.debug(f'Время подключения к "{hostname}": {time() - start_connect_time} секунд.')

        if log_file_path and Path(log_file_path).exists():
            await convert_to_utf8(log_file_path)  # Convert file to UTF-8 if needed
            sma_data_list = await log_parser(log_file_path)
            pprint(sma_data_list)

        # Обновить статус сервера
        await update_server_status(hostname, log_file_path)

    except Exception as e:
        logger.error(f'Ошибка при обработке магазина {shop_id}: {e}')
        # Обновить статус сервера при ошибке
        await update_server_status(hostname, False)


# async def process_file(file: str, pattern: str):
#     await convert_to_utf8(file)  # Convert file to UTF-8 if needed
#     await log_parser_runner(file, pattern)


async def run():
    now = dt.now()
    formatted_date_time = now.strftime('on %Y.%m.%d at %H:%M')

    logger.info(f'Скрипт запущен в {formatted_date_time}.')

    while True:
        start_cycle_time = time()

        tasks = [aio_create_task(perform_smb_task(shop_id)) for shop_id in SHOPS]
        # Ждем завершения всех задач
        await aio_gather(*tasks)

        # tasks = [aio_create_task(process_file(os_join(LOG_SMP_PATH, f'{shop_id}.log'))) for shop_id in SHOPS]
        # # Ждем завершения всех задач
        # await aio_gather(*tasks)

        logger.info(f'Время выполнения цикла: {time() - start_cycle_time} секунд.')
        logger.info(f'Пауза на: {SMB_SLEEP_INTERVAL} секунд')
        await aio_sleep(SMB_SLEEP_INTERVAL)


if __name__ == '__main__':
    aio_run(run())
