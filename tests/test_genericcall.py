from datetime import datetime
import unittest as ut
from discord_dumper.utils import GenericCall


class TestGenericCall(ut.TestCase):
    def test_instancing(self):
        call = GenericCall(
            "TestCaller",
            "TestFriend",
            "29-Oct-2021 1:43 PM",
            "Started a call that lasted 69 minutes.",
        )

        self.assertEqual(call.caller, "TestCaller")
        self.assertEqual(call.to, "TestFriend")
        self.assertEqual(call.service_message, "Started a call that lasted 69 minutes.")

    def test_date(self):
        call = GenericCall(
            "TestCaller",
            "TestFriend",
            "29-Oct-2021 1:43 PM",
            "Started a call that lasted 69 minutes.",
        )

        self.assertEqual(call.date["date"], "29/10/2021")
        self.assertEqual(call.date["time"], "13:43")

    def test_duration(self):
        call = GenericCall(
            "TestCaller",
            "TestFriend",
            "29-Oct-2021 1:43 PM",
            "Started a call that lasted 69 minutes.",
        )

        dur = call.get_duration()

        self.assertEqual(dur, 69)

    def test_to_csv(self):
        call = GenericCall(
            "TestCaller",
            "TestFriend",
            "29-Oct-2021 1:43 PM",
            "Started a call that lasted 69 minutes.",
        )

        self.assertEqual(
            call.to_csv(), '"TestCaller","TestFriend","29/10/2021","13:43","69 minutes"'
        )
