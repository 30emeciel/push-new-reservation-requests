import logging
import os

import firebase_admin
from box import Box
from firebase_admin import credentials
from firebase_admin import firestore
# Use the application default credentials
from slack_sdk import WebClient

from slack_messages import generate_new_reservation_slack_message

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': "trentiemeciel",
})

log = logging.getLogger(__name__)
db = firestore.client()
slack = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
slack_channel = os.environ['SLACK_CHANNEL']


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

    push_new_reservation_request_to_slack(resource_string)


def push_new_reservation_request_to_slack(doc_path):
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
    txt = generate_new_reservation_slack_message(data)

    slack.chat_postMessage(
        channel=slack_channel,
        text=txt,
        link_names=False,
        attachments=[]
    )


