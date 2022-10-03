import unittest
import pandas as pd
from twilio.rest import Client
from twilio_connector import Twilio


class TestTwilio(unittest.TestCase):
    def setUp(self) -> None:
        self.args = []
        # read text file containing required arguments on each line
        with open("arguments.txt") as f:
            self.args.append(f.readline())
        self.twilio = Twilio(self.args[0], self.args[1])


class TestGetConversation(TestTwilio):
    def test_return_type(self):
        """Checks if the function returns list"""
        self.assertIsInstance(
            self.twilio.get_conversation(self.args[2], self.args[3]), list
        )


class TestAddMessage(TestTwilio):
    def test_return_type(self):
        """Checks if add message is working properly"""
        self.test_message = ["author", "this is test message"]
        self.twilio.add_message(
            self.args[2], self.test_message[0], self.test_message[1]
        )
        self.messages = self.twilio.get_conversation(self.args[2], 1)
        requested_msg = []
        for msg in self.messages:
            requested_msg.append(msg.author)
            requested_msg.append(msg.body)
        self.assertEqual(
            requested_msg,
            self.test_message,
            f"Requested message {requested_msg} does not match the test message",
        )
