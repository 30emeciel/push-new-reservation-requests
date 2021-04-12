from datetime import datetime, timezone

from box import Box
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    from message_templates import generate_new_reservation_slack_message

    pax = Box({
        "name": "Pax name"
    })
    request = Box({
        "kind": "COLIVING",
        "arrival_date": datetime(2021, 2, 19, tzinfo=timezone.utc),
        "departure_date": datetime(2021, 3, 1, tzinfo=timezone.utc),
        "number_of_nights": 3,
    })
    data = {
        "pax": pax,
        "request": request,
    }
    txt = generate_new_reservation_slack_message(data)
    import slack_message
    slack_message.send_slack_message(txt)



