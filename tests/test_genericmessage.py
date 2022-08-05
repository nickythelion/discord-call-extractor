from datetime import datetime
import unittest as ut
from discord_dumper.utils import GenericMessage


class TestGenericMessage(ut.TestCase):
    def test_instancing(self):

        msg = GenericMessage(
            "TestSender",
            "TestRecipient",
            "29-Oct-2021 1:43 PM",
            "This is a test content",
            "TestAttach.png",
        )
        self.assertEqual(msg.author, "TestSender")
        self.assertEqual(msg.to, "TestRecipient")
        self.assertEqual(msg.content, "This is a test content")
        self.assertEqual(msg.attachments, "TestAttach.png")

        msg_no_attach = GenericMessage(
            "TestSender2",
            "TestRecipient2",
            "29-Oct-2021 1:43 PM",
            "This is a test content as well",
            None,
        )
        self.assertEqual(msg_no_attach.author, "TestSender2")
        self.assertEqual(msg_no_attach.to, "TestRecipient2")
        self.assertEqual(msg_no_attach.content, "This is a test content as well")
        self.assertEqual(msg_no_attach.attachments, None)

    def test_date(self):

        msg = GenericMessage(
            "TestSender",
            "TestRecipient",
            "29-Oct-2021 1:43 PM",
            "This is a test content",
            None,
        )

        self.assertIsInstance(msg.timestamp, datetime)

        self.assertEqual(msg.timestamp.__str__(), "2021-10-29 13:43:00")

        self.assertEqual(msg.date["date"], "29/10/2021")
        self.assertEqual(msg.date["time"], "13:43")

    def test_to_csv(self):
        msg = GenericMessage(
            "TestSender",
            "TestRecipient",
            "29-Oct-2021 1:43 PM",
            "This is a test content",
            None,
        )

        out = msg.to_csv()

        self.assertEqual(
            out,
            '"TestSender","TestRecipient","29/10/2021","13:43","This is a test content",""',
        )


if __name__ == "__main__":
    ut.main()
