import logging

from box import Box
from core import firestore_client
from core.slack_message import SlackSender
from core.tpl import render

log = logging.getLogger(__name__)

db = firestore_client.db()
slack_sender = SlackSender()


def from_firestore(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    resource_string = context.resource

    # print out the resource string that triggered the function
    print(f"Function triggered by change to: {resource_string}.")
    # now print out the entire event object
    print(str(event))

    push_new_reservation_request_to_slack(resource_string, Box(event))


def push_new_reservation_request_to_slack(doc_path, event):
    request_ref = db.document(doc_path)
    pax_ref = request_ref.parent.parent
    pax_doc, request_doc = pax_ref.get(), request_ref.get()
    assert pax_doc.exists and request_doc.exists

    request = Box(request_doc.to_dict())
    pax = Box(pax_doc.to_dict())
    if request.state != "PENDING_REVIEW":
        log.info(f"request 'state' != PENDING_REVIEW, ignoring")
        return

    data = {
        "pax": pax,
        "request": request
    }
    txt = render("new_reservation_fr.txt", data)

    slack_sender.send_slack_message(txt)


