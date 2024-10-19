import json
from pathlib import Path
import re


# Асинхронная функция для обработки строк и формирования JSON
async def create_json_from_lines(lines, log_file):
    # Регулярное выражение для поиска строк по новому шаблону
    pattern = re.compile(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2} \w+ заказ \d+_\d+\.\w+ \w+")

    # Структура для хранения данных
    data = {}

    # Проходим по строкам и добавляем данные, соответствующие шаблону
    for line in lines:
        if pattern.match(line):
            parts = line.strip().split()
            timestamp = f'{parts[0]} {parts[1]}'
            status = parts[2] + " " + parts[3]  # Например: "Новый заказ" или "Удален заказ"
            order = parts[4].split('_')
            order_number = order[0]
            creator_id = order[1].split('.')[0]
            user_login = parts[5]

            # Получаем идентификатор магазина из имени файла
            shop_id = Path(log_file).stem

            # Обновляем структуру данных
            if shop_id not in data:
                data[shop_id] = {"creators": {}}

            if creator_id not in data[shop_id]["creators"]:
                data[shop_id]["creators"][creator_id] = {"user_login": user_login, "orders": {}}

            if order_number not in data[shop_id]["creators"][creator_id]["orders"]:
                data[shop_id]["creators"][creator_id]["orders"][order_number] = []

            # Добавляем новое событие в историю заказа
            data[shop_id]["creators"][creator_id]["orders"][order_number].append({
                "order_status": status,
                "timestamp": timestamp
            })

    # Преобразуем данные в формат JSON
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    return json_data


if __name__ == '__main__':
    # Пример использования
    async def test_main():
        lines = "17.08.2024 11:11:56 Новый заказ 00000714_013400000043.ZAK afonina"
        log_file = "TST-01.log"
        json_result = await create_json_from_lines(lines, log_file)
        print(json_result)

        lines = [
            '17.08.2024 11:11:56 Новый заказ 00000714_013400000043.ZAK afonina',
            '17.08.2024 12:44:38 Новый заказ 00000715_013400000043.ZAK afonina',
            '17.08.2024 13:51:35 Новый заказ 00000716_013400000043.ZAK afonina',
            '17.08.2024 13:54:18 Новый заказ 00000718_013400000043.ZAK afonina',
            '17.08.2024 13:54:50 Удален заказ 00000716_013400000043.ZAP afonina',
            '17.08.2024 14:12:32 Новый заказ 00000719_013400000043.ZAK afonina',
            '17.08.2024 15:34:57 Новый заказ 00000720_013400000043.ZAK afonina',
            '17.08.2024 15:49:37 Новый заказ 00000721_013400000043.ZAK afonina',
            '17.08.2024 16:07:27 Новый заказ 00000722_013400000043.ZAK afonina',
        ]
# 17.08.2024 15:56:39 404 - Объект не найден: GET /api/v1/order?filename=00000721_013400000043.ZAK HTTP/1.1 afonina

        log_file = "TST-01.log"
        json_result = await create_json_from_lines(lines, log_file)
        print(json_result)

    # Запуск асинхронного кода
    from asyncio import run as async_run
    async_run(test_main())

