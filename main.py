import logging
from os import environ

import firebase_admin
from dotmap import DotMap
from firebase_admin import credentials
from firebase_admin import firestore
# Use the application default credentials
from slack_sdk import WebClient

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': "trentiemeciel",
})

log = logging.getLogger(__name__)
db = firestore.client()
slack = WebClient(token=environ['SLACK_BOT_TOKEN'])


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

    request_data = DotMap(request_doc.to_dict(), _dynamic=False)
    pax_data = DotMap(pax_doc.to_dict(), _dynamic=False)
    if request_data.state != "PENDING_REVIEW":
        log.info(f"request 'state' != PENDING_REVIEW, ignoring")
        return

    text = f"""\
Nouvelle réservation de {pax_data.name}, produit {request_data.kind} \
du <!date^{int(request_data.arrival_date.timestamp())}^{{date_long}}|NA> \
au <!date^{int(request_data.departure_date.timestamp())}^{{date_long}}|NA> \
({request_data.number_of_nights} nuits)
"""
    slack.chat_postMessage(
        channel='null',
        text=text,
        link_names=False,
        attachments=[]
    )
