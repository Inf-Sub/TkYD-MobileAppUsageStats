__author__ = 'InfSub'
__contact__ = 'ADmin@TkYD.ru'
__copyright__ = 'Copyright (C) 2024, [LegioNTeaM] InfSub'
__date__ = '2024/10/19'
__deprecated__ = False
__email__ = 'ADmin@TkYD.ru'
__maintainer__ = 'InfSub'
__status__ = 'Production'
__version__ = '2.2.10'

from re import compile as re_compile

from app.utils.utils import aio_open, Path, type_Dict, type_List, getenv, logging


logger = logging.getLogger(__name__)


FIND_TEXT_PATTERN = getenv('FIND_TEXT_PATTERN')


async def log_parser(log_file: str, pattern: str = '') -> type_List[type_Dict]:
    # Регулярное выражение для поиска строк по новому шаблону
    pattern = re_compile(pattern if pattern else FIND_TEXT_PATTERN)

    # Список для хранения данных
    data_list = []

    # Открываем файл в режиме чтения
    async with aio_open(log_file, 'r', encoding='utf-8') as file:
        # Читаем все строки из файла
        lines = await file.readlines()

    # Получаем идентификатор магазина из имени файла
    shop_id = Path(log_file).stem

    # Проходим по строкам и добавляем данные, соответствующие шаблону
    for line in lines:
        match = pattern.match(line)
        if match:
            parts = line.strip().split()
            try:
                timestamp = f'{parts[0]} {parts[1]}'
                status = parts[2]
                order_info = parts[4].split('_')
                order_number = order_info[0]
                creator_id = order_info[1].split('.')[0]
                user_login = parts[5]

                record = {
                    "shop_id": shop_id,
                    "creator_id": creator_id,
                    "user_login": user_login,
                    "order_number": order_number,
                    "order_status": status,
                    "timestamp": timestamp
                }

                data_list.append(record)
            except IndexError as e:
                logger.error(f"Error processing line: {line}. Error: {e}")

    return data_list


if __name__ == '__main__':
    from app.utils.utils import aio_run, aio_gather, os_join, getenv, pprint

    from app.config import REPO_DIR


    async def test_run():
        shops = getenv('SHOPS').replace(' ', '').split(',')
        load_to_path = os_join(REPO_DIR, getenv('LOAD_TO_PATH'))

        tasks = []
        for shop_id in shops:
            shop_log_file = os_join(load_to_path, '{}.log'.format(shop_id))
            print(shop_log_file)
            if Path(shop_log_file).exists():
                print(f'File: "{shop_log_file}" - exist. Read file...')
                tasks.append(log_parser(shop_log_file))
            else:
                print(f'File: "{shop_log_file}" - does not exist')

        results_list = await aio_gather(*tasks)
        return results_list


    # Вызов функции test_run и получение результатов
    results = aio_run(test_run())
    for result in results:
        pprint(result)
