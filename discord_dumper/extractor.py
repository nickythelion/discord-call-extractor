import csv
import os
import sys
from typing import List
from discord_dumper.utils import (
    CSVWriteError,
    GenericCall,
    GenericMessage,
    CSVFileError,
)


def __check_csv_path(path: str) -> bool:
    """Checs if path to CSV file is valid

    Args:
        path (str): path to check

    Returns:
        bool: a boolean determining is a given path is valid
    """

    return (
        os.path.exists(path)
        and os.path.isfile(path)
        and os.path.splitext(path)[1] == ".csv"
    )


def __get_recipient(sender: str) -> str:
    """Gets the recipient of a message/call

    Args:
        sender (str): A person who sent the message

    Returns:
        str: A string containing the name of a recipient. If sender's name is not within a limited range of options, an empty string is returned
    """
    if sender not in [
        "AFRY (The Australian One)#7451",
        "Nicky (the russian one)#4173",
    ]:
        return ""

    return (
        "Nicky (the russian one)#4173"
        if sender == "AFRY (The Australian One)#7451"
        else "AFRY (The Australian One)#7451"
    )


def __get_records(csv_path: str) -> List[GenericMessage | GenericCall]:
    """Gets all the records from a CSV file and returns an array filled with corresponding classes

    Args:
        csv_path (str): path to the csv file

    Raises:
        CSVFileError: raised if path points to nothing, to something that is not a file or to a file with an unsupported extension

    Returns:
        List[GenericMessage | GenericCall]: _description_
    """

    if not __check_csv_path(csv_path):
        raise CSVFileError(
            f"File {csv_path} does not exist, not a file or has an unsupported format"
        )

    line_count = 0

    out = []

    with open(csv_path, encoding="utf-8") as db:
        reader = csv.reader(db)

        for row in reader:
            if line_count == 0:
                line_count += 1
                continue

            if row[3].find("Started a call") != -1:
                out.append(
                    GenericCall(
                        row[1], __get_recipient(row[1]), row[2], row[3]
                    )
                )
                line_count += 1
                continue

            out.append(
                GenericMessage(
                    row[1], __get_recipient(row[1]), row[2], row[3], row[4]
                )
            )

    return out


def get_calls(db_path: str) -> List[GenericCall]:
    """Gets call history from a CSV database

    Args:
        db_path (str): path to a csv file

    Returns:
        List[GenericCall]: List containing all the call records
    """
    records = __get_records(db_path)
    return list(filter(lambda rec: isinstance(rec, GenericCall), records))


def get_messages(db_path: str) -> List[GenericMessage]:
    """Gets all the messages from a CSV database

    Args:
        db_path (str): path to a csv file

    Returns:
        List[GenericMessage]: List containing all the messages
    """
    records = __get_records(db_path)
    return list(filter(lambda rec: isinstance(rec, GenericMessage), records))


def write_to_csv(
    path: str,
    headers: List[str],
    items: List[GenericCall] | List[GenericMessage],
) -> None:
    """Writes data to a CSV file.

    Args:
        path (str): path to a file. If file already exists, the fucntion will prompt the user.
        headers (List[str]): CSV headers to write at the first line of the file
        items (List[GenericCall] | List[GenericMessage]): rows to write

    Raises:
        CSVWriteError: raised if the type of items is not homogenous
        CSVFileError: raised if path points to a non-csv file
    """
    if (not all([isinstance(x, GenericCall) for x in items])) and (
        not all([isinstance(x, GenericMessage) for x in items])
    ):
        raise CSVWriteError(
            f"Cannot write records of multiple types into one csv file"
        )

    if os.path.exists(path) and not os.path.isfile(path):
        raise CSVFileError(f"{path} is not a file")

    if os.path.splitext(path)[1] != ".csv":
        raise CSVFileError("Cannot write to a non-csv file")

    if os.path.exists(path):
        answer = input(
            f"Warning! File {path} already exists. If continued, the contents of this file will be overwritten. Procced [Y/n]? "
        ).lower()

        if answer == "n":
            print("Aborted by the user!")
            sys.exit(1)
        elif answer == "y":
            print(f"Erasing the contents of {path}")
        else:
            print(f"Unknown choice: {answer}")
            sys.exit(-1)

    else:
        with open(path, "x", encoding="utf-8"):
            pass

    with open(path, "w", encoding="utf-8") as db:
        db.write(f'{",".join(headers)}\n')

        for item in items:
            db.write(f"{item.to_csv()}\n")
