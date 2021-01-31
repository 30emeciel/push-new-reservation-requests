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


SLACK_DATE_FORMAT = "date"


def slack_data_format(dt):
    return f"<!date^{int(dt.timestamp())}^{{{SLACK_DATE_FORMAT}}}|NA>"


def coliving_request_format(request):
    return f"""\
du {slack_data_format(request.arrival_date)} \
au {slack_data_format(request.departure_date)} \
({request.number_of_nights} nuit{"s" if request.number_of_nights > 1 else ""})\n
"""


def coworking_request_format(request):
    return f"""\
le {slack_data_format(request.arrival_date)}\
"""


def push_new_reservation_request_to_slack(doc_path):
    request_ref = db.document(doc_path)
    pax_ref = request_ref.parent.parent
    pax_doc, request_doc = pax_ref.get(), request_ref.get()
    assert pax_doc.exists and request_doc.exists

    request = DotMap(request_doc.to_dict(), _dynamic=False)
    pax = DotMap(pax_doc.to_dict(), _dynamic=False)
    if request.state != "PENDING_REVIEW":
        log.info(f"request 'state' != PENDING_REVIEW, ignoring")
        return

    text = f"""\
Nouvelle réservation de *{pax.name}*, produit *{request.kind}* :\n"""

    text += coliving_request_format(request) if request.kind == "COLIVING" else coworking_request_format(request)

    slack.chat_postMessage(
        channel='null',
        text=text,
        link_names=False,
        attachments=[]
    )
