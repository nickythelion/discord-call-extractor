from typing import List
import unittest as ut
from discord_dumper.extractor import get_calls, get_messages, write_to_csv
from discord_dumper.utils import (
    CSVFileError,
    CSVWriteError,
    GenericCall,
    GenericMessage,
)


class TestExtractor(ut.TestCase):
    def test_get_calls_invalid_paths(self):

        db_path_nonexistent = "./test_data/test_data_does_not_exist.csv"
        db_path_not_a_file = "./test_data"
        db_path_invalid_ext = "./test_data/test_data_wrong_ext.wrong"

        with self.assertRaises(CSVFileError):
            get_calls(db_path_nonexistent)

        with self.assertRaises(CSVFileError):
            get_calls(db_path_not_a_file)

        with self.assertRaises(CSVFileError):
            get_calls(db_path_invalid_ext)

    def test_get_calls(self):
        db_path = "tests/test_data/test_data.csv"

        calls = get_calls(db_path)

        self.assertNotEqual(len(calls), 0)
        self.assertEqual(calls[0].get_duration(), 63)

    def test_get_messages_invalid_paths(self):
        db_path_nonexistent = "./test_data/test_data_does_not_exist.csv"
        db_path_not_a_file = "./test_data"
        db_path_invalid_ext = "./test_data/test_data_wrong_ext.wrong"

        with self.assertRaises(CSVFileError):
            get_messages(db_path_nonexistent)

        with self.assertRaises(CSVFileError):
            get_messages(db_path_not_a_file)

        with self.assertRaises(CSVFileError):
            get_messages(db_path_invalid_ext)

    def test_get_messages(self):
        db_path = "./tests/test_data/test_data.csv"

        messages = get_messages(db_path)

        self.assertNotEqual(len(messages), 0)
        self.assertEqual(messages[0].author, "Nicky (the bi one) 🇷🇺#4173")

    def test_write_to_csv_invalid_data(self):
        db_path_dir = "./test_output/"
        db_path_wrong_ext = "./test_output/wrong_format.ext"

        generic_call_obj = GenericCall(
            "Me",
            "You",
            "29-Oct-21 07:21 PM",
            "Started a call that laster 13 minutes",
        )

        generic_message_obj = GenericMessage(
            "Me", "You", "29-Oct-21 07:21 PM", "This is a test message", None
        )

        with self.assertRaises(CSVFileError):
            write_to_csv(
                db_path_dir,
                ["Test", "Headers"],
                list([generic_call_obj]),
            )

        with self.assertRaises(CSVFileError):
            write_to_csv(
                db_path_wrong_ext, ["Test", "Headers"], [generic_call_obj]
            )

        invalid_data_chunks = [generic_call_obj, generic_message_obj]
        headers = ["Caller", "Recipient", "Date", "Time", "Duration"]

        with self.assertRaises(CSVWriteError):
            write_to_csv("./test_output/t.csv", headers, invalid_data_chunks)
