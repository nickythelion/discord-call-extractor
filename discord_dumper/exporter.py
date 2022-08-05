from datetime import date, datetime
import os
from time import mktime, time
from typing import List

from bs4 import BeautifulSoup
from discord_dumper.utils import GenericCall, GenericMessage, TemplateError
from discord_dumper.extractor import get_calls, get_messages, write_to_csv


def __check_path(path: str) -> bool:
    return (
        os.path.exists(path)
        and os.path.isfile(path)
        and os.path.splitext(path)[1] in [".html", ".htm"]
    )


def __load_template(path: str) -> BeautifulSoup:
    if not __check_path(path):
        raise TemplateError(
            f"Cannot load template from {path}: it either does not exist, is not a file or has an unsupported format"
        )

    with open(path, "r") as file:
        raw_html = file.read()

    handler = BeautifulSoup(raw_html, "html.parser")

    return handler


def export_messages(messages: List[GenericMessage]) -> str:
    raise NotImplementedError("This function has not yet been implemented")


def export_calls(calls: List[GenericCall]):
    template = __load_template("./templates/calls.html")

    call_table = template.find(id="call-logs-table")

    row_num = 1

    for call in calls:
        row_id = template.new_tag("td", attrs={"class": "clt-item"})
        row_id.string = str(row_num)

        date_and_time = template.new_tag("td", attrs={"class": "clt-item"})
        date_and_time.string = f"{call.date['date']}, {call.date['time']}"

        caller = template.new_tag("td", attrs={"class": "clt-item"})
        caller.string = call.caller

        recipient = template.new_tag("td", attrs={"class": "clt-item"})
        recipient.string = call.to

        call_duration = template.new_tag("td", attrs={"class": "clt-item"})
        call_duration.string = f"{call.get_duration()} minutes"

        row = template.new_tag("tr", attrs={"class": "clt-row"})
        row.append(row_id)
        row.append(date_and_time)
        row.append(caller)
        row.append(recipient)
        row.append(call_duration)

        call_table.append(row)
        row_num += 1

    timestamp = template.find(id="timestamp-date")
    timestamp_raw = datetime.now()
    timestamp_raw_unix = mktime(timestamp_raw.timetuple())
    timestamp.string = datetime.strftime(timestamp_raw, "%d/%m/%Y @ %H:%M")

    out_path = f"output/calls-{str(timestamp_raw_unix).split('.')[0]}.html"

    with open(out_path, "xb") as output:
        output.write(template.prettify("utf-8"))

    return out_path
