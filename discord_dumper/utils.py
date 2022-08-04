import datetime as dtime
import re
from types import SimpleNamespace
from typing import Any

class GenericMessage:

    def __init__(self, sender: str, to: str, date_string: str, content: str, attachments: str | None) -> None:
        """Creates a GenericMessage object

        Args:
            sender (str): a person who sent the message
            to (str): a recipient of a message
            date_string (str): a date and time of when the message was sent
            content (str): message itself
            attachments (str | None): attachments
        """
        
        self.DATE_FORMAT_CONST = "%d-%b-%y %I:%M %p"

        self.author = sender
        self.to = to

        # This breakdown is needed for more efficient CSV dump later
        
        self.timestamp = dtime.datetime.strptime(date_string, self.DATE_FORMAT_CONST)
        self.date = {
            "date": dtime.datetime.strftime(self.timestamp, "%d/%m/%Y"),
            "time": dtime.datetime.strftime(self.timestamp, "%H:%M")
        }

        self.content = content
        self.attachments = attachments
    
    def to_csv(self) -> str:
        return f"\"{self.author}\",\"{self.to}\",\"{self.date['date']}\",\"{self.date['time']}\",\"{self.content}\",\"{self.attachments if self.attachments else ''}\""


class GenericCall:
    def __init__(self, caller: str, to: str, date_string: str, service_message: str) -> None:
        """Creates a GenericCall object

        Args:
            caller (str): The personwho initiated the call
            to (str): The person who received the call
            date_string (str): When the call was made
            service_message (str): The service message from Discord (... Started a call...)
        """

        self.DATE_FORMAT_CONST = "%d-%b-%y %I:%M %p"

        self.caller = caller
        self.to = to

        # This breakdown is needed for more efficient CSV dump later
        
        self.timestamp = dtime.datetime.strptime(date_string, self.DATE_FORMAT_CONST)
        self.date = {
            "date": dtime.datetime.strftime(self.timestamp, "%d/%m/%Y"),
            "time": dtime.datetime.strftime(self.timestamp, "%H:%M")
        }
        self.service_message = service_message

    def get_duration(self) -> int:
        """Get the duration of the call

        Returns:
            int: the duration of the call in minutes
        """

        re_pattern = re.compile(r'\d+')

        dur = int(re.findall(re_pattern, self.service_message)[0])

        return dur

    def to_csv(self) -> str:

        return f"\"{self.caller}\",\"{self.to}\",\"{self.date['date']}\",\"{self.date['time']}\",\"{self.get_duration()} minutes\""

