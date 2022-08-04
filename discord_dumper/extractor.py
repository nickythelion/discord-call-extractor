import csv
import os
import sys
from typing import List

from discord_dumper.utils import GenericCall, GenericMessage

def parse_records(csv_path: str) -> List[GenericCall | GenericMessage]:
    """Reads the CSV file

    Args:
        csv_path (str): path to the file

    Returns:
        List[GenericCall | GenericMessage]: List containing the records
    """

    if (not os.path.exists(csv_path) or not os.path.isfile(csv_path)):
        raise FileNotFoundError(f'File {csv_path} could not be found')

    buf = []

    line_count = 0

    with open(csv_path, encoding="utf-8") as db:
        reader = csv.reader(db)

        for row in reader:
            if line_count == 0:
                line_count += 1
                continue

            if row[3].find("Started a call") != -1:
                buf.append(GenericCall(row[1], "Nicky (the bi one) 🇷🇺#4173" if row[1] == "Spazdikcnt#7451" else "Spazdikcnt#7451", row[2], row[3]))
            else:
                buf.append(GenericMessage(row[1], "Nicky (the bi one) 🇷🇺#4173" if row[1] == "Spazdikcnt#7451" else "Spazdikcnt#7451", row[2], row[3], row[4] if row[4] else None))

            line_count += 1

    return buf

def _write_to_calls_db(csv_path: str, items: List[GenericCall | GenericMessage]) -> None:

    is_file_good = os.path.exists(csv_path) or os.path.isfile(csv_path)

    if (is_file_good):
        res = input(f"Warning! File {csv_path} already exists and will be overwritten. Proceed [Y/n]? ").lower()

        if (res == "n"):
            print("Aborted")
            sys.exit(1)
        elif (res == "y"):
            pass
        else:
            print('Unknown choice')
            sys.exit(-1)

    items = filter(lambda item: isinstance(item, GenericCall), items)

    with open(csv_path, "w" if is_file_good else "x", encoding="utf-8") as db:
        db.write("Caller,Recipient,Date,Time,Duration\n")

        for i in items:
            db.write(i.to_csv() + "\n")

def _write_to_messages_db(csv_path: str, items: List[GenericCall | GenericMessage]) -> None:

    is_file_good = os.path.exists(csv_path) or os.path.isfile(csv_path)

    if (is_file_good):
        res = input(f"Warning! File {csv_path} already exists and will be overwritten. Proceed [Y/n]? ").lower()

        if (res == "n"):
            print("Aborted")
            sys.exit(1)
        elif (res == "y"):
            pass
        else:
            print('Unknown choice')
            sys.exit(-1)

    items = filter(lambda item: isinstance(item, GenericMessage), items)

    with open(csv_path, "w" if is_file_good else "x", encoding="utf-8") as db:
        db.write("Author,Recipient,Date,Time,Content,Attachments\n")

        for i in items:
            db.write(i.to_csv() + "\n")

def write_to_separate_dbs(name: str, items: List[GenericMessage | GenericCall]) -> None:
    _write_to_calls_db(f"{name}_calls.csv", items)
    _write_to_messages_db(f"{name}_messages.csv", items)