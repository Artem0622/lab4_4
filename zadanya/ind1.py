#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
import pathlib
import logging
import time

# Настройка логирования
log_format = '%(asctime)s.%(msecs)d - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('flights.log', mode='a')  # Логирование в файл с именем 'flights.log'
    ]
)

# Создать родительский парсер для определения имени файла.
file_parser = argparse.ArgumentParser(add_help=False)
file_parser.add_argument(
    "filename",
    action="store",
    help="Имя файла с данными"
)

# Создать основной парсер командной строки.
parser = argparse.ArgumentParser("flights")
parser.add_argument(
    "--version",
    action="version",
    version="%(prog)s 0.1.0"
)

subparsers = parser.add_subparsers(dest="command")

# Создать субпарсер для добавления рейса.
add = subparsers.add_parser(
    "add",
    parents=[file_parser],
    help="Добавить новый рейс"
)
add.add_argument(
    "-d",
    "--destination",
    action="store",
    required=True,
    help="Пункт назначения рейса"
)
add.add_argument(
    "-n",
    "--number",
    action="store",
    type=int,
    required=True,
    help="Номер рейса"
)
add.add_argument(
    "-t",
    "--type",
    action="store",
    required=True,
    help="Тип самолета"
)

# Создать субпарсер для отображения всех рейсов.
_ = subparsers.add_parser(
    "display",
    parents=[file_parser],
    help="Отобразить все рейсы"
)

# Создать субпарсер для выбора рейсов.
select = subparsers.add_parser(
    "select",
    parents=[file_parser],
    help="Выбрать рейсы"
)
select.add_argument(
    "-s",
    "--select",
    action="store",
    required=True,
    help="Необходимый выбор"
)


def add_flight(flights, dst, nmb, tpe):
    try:
        flights.append(
            {
                "destination": dst,
                "number_flight": nmb,
                "type_plane": tpe
            }
        )
        logging.info("Рейс успешно добавлен")
    except Exception as e:
        logging.error(f"Ошибка при добавлении рейса: {e}")
    return flights


def display_flights(flights):
    try:
        for flight in flights:
            print(flight)
    except Exception as e:
        logging.error(f"Ошибка при отображении рейсов: {e}")


def select_flights(flights, t):
    try:
        result = [flight for flight in flights if t in str(flight.values())]
        return result
    except Exception as e:
        logging.error(f"Ошибка при выборе рейсов: {e}")


def save_flights(file_name, flights):
    try:
        with open(file_name, "w", encoding="utf-8") as fout:
            json.dump(flights, fout, ensure_ascii=False, indent=4)
        logging.info("Данные успешно сохранены в файл")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных в файл: {e}")


def load_flights(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as fin:
            return json.load(fin)
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных из файла: {e}")
        return []


def main(command_line=None):
    try:
        start_time = time.time()
        args = parser.parse_args(command_line)
        dst = pathlib.Path(args.filename)
        is_dirty = False
        if dst.exists():
            flights = load_flights(dst)
        else:
            flights = []

        if args.command == "add":
            flights = add_flight(
                flights,
                args.destination,
                args.number,
                args.type
            )
            is_dirty = True

        elif args.command == "display":
            display_flights(flights)

        elif args.command == "select":
            selected_flights = select_flights(flights, args.select)
            display_flights(selected_flights)

        if is_dirty:
            save_flights(dst, flights)

        elapsed_time = time.time() - start_time
        logging.info(f"Время выполнения команды: {elapsed_time:.3f} секунд ")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    main()
