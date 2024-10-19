__author__ = 'InfSub'
__contact__ = 'ADmin@TkYD.ru'
__copyright__ = 'Copyright (C) 2024, [LegioNTeaM] InfSub'
__date__ = '2024/10/19'
__deprecated__ = False
__email__ = 'ADmin@TkYD.ru'
__maintainer__ = 'InfSub'
__status__ = 'Development'
__version__ = '2.2.10'


from re import compile as re_compile

from app.utils.utils import type_Dict, type_List, getenv, logger

FIND_TEXT_PATTERN = getenv('FIND_TEXT_PATTERN')


# Асинхронная функция для обработки строк и формирования списка словарей
async def create_dict_from_lines(lines: type_List[str], shop_id: str, pattern: str = '') -> type_List[type_Dict]:
    # Регулярное выражение для поиска строк по новому шаблону
    pattern = re_compile(pattern if pattern else FIND_TEXT_PATTERN)

    # Список для хранения данных
    data_list = []

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
    from app.utils.utils import aio_run, pprint

    # Пример использования
    async def test_main():
        lines = [
            '17.08.2024 13:51:35 Новый заказ 00000716_013400000043.ZAK afonina',
            '17.08.2024 13:54:18 Новый заказ 00000718_013400000043.ZAK afonina',
            '17.08.2024 13:54:50 Удален заказ 00000716_013400000043.ZAP afonina',
            '17.08.2024 14:12:32 Новый заказ 00000719_013400000043.ZAK afonina',
            '29.09.2024 15:21:45 Новый заказ 00000876_013400000026.ZAK neboga',
            '29.09.2024 15:26:25 Новый заказ 00000877_013400000043.ZAK afonina',
            '29.09.2024 17:48:23 Новый заказ 00000882_013400000015.ZAK bahtuzina',
            '29.09.2024 18:36:32 Новый заказ 00000883_013400000026.ZAK neboga',
            '01.10.2024 11:55:41 Новый заказ 00000890_013400000015.ZAK bahtuzina',
            '01.10.2024 11:56:21 Удален заказ 00000890_013400000015.ZAP bahtuzina',
        ]
        log_file = "TST-01.log"
        result_data = await create_dict_from_lines(lines, log_file)
        pprint(result_data, indent=4)

    # Запуск асинхронного кода
    aio_run(test_main())
