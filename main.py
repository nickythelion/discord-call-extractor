import sys
from discord_dumper.exporter import export_calls
from discord_dumper.extractor import get_calls, get_messages, write_to_csv


def main() -> None:
    print("Getting data from a csv file")

    print("Filtering call data")
    call_list = get_calls("data/raw-db-calls-messages-arfy.csv")

    print("Filtering message data")
    message_list = get_messages("data/raw-db-calls-messages-arfy.csv")

    print("Forming headers")
    call_headers = ["Caller", "Recipient", "Date", "Time", "Duration"]
    msg_headers = [
        "Author",
        "Recipient",
        "Date",
        "Time",
        "Content",
        "Attachments",
    ]

    print("Writing calls to a separate csv file")
    write_to_csv("output/data-calls.csv", call_headers, call_list)

    print("Writing message data to a separate file")
    write_to_csv("output/data-messages.csv", msg_headers, message_list)

    ans = input("Export calls to an HTML template? [Y/n] ").lower()

    if ans not in ["y", "n"]:
        print("Unknown choice\nAborting")
        sys.exit(1)

    if ans == "n":
        print("Skipped\nExiting")
        sys.exit(0)

    output_path = export_calls(call_list)
    print(f"Calls were exported to {output_path}")
    print("Exiting")
    sys.exit(0)


if __name__ == "__main__":
    main()
