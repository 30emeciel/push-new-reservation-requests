from os import environ
import requests
from dotmap import DotMap
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': "trentiemeciel",
})
import google

client = firestore.Client()

class FirestoreEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, google.api_core.datetime_helpers.DatetimeWithNanoseconds):
            return obj.rfc3339()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def from_firestore(data, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    resource_string = context.resource

    # print out the resource string that triggered the function
    print(f"Function triggered by change to: {resource_string}.")
    # now print out the entire event object
    print(str(data))



    post_new_reservation_request_to_zapier(resource_string)


def post_new_reservation_request_to_zapier(docpath):
    path_parts = docpath.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])

    request_ref = client.document(docpath)
    pax_ref = request_ref.parent.parent
    pax_doc, request_doc = pax_ref.get(), request_ref.get()
    assert pax_doc.exists and request_doc.exists
    
    url = environ.get(
        "ZAPIER_WEBHOOK_URL",
        "https://hooks.zapier.com/hooks/catch/632541/o0va7mw/"
    )

    data = {
      "pax": pax_doc.to_dict(),
      "request": request_doc.to_dict()
    }
    json_str = json.dumps(data, cls=FirestoreEncoder)
    resp = requests.post(url, json_str, headers={"content-type": "application/json"})
    resp.raise_for_status()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    # export GOOGLE_APPLICATION_CREDENTIALS="trentiemeciel.json"
    # get the token using postman
    data = {
        "fields": {
            'arrivalDate': {'timestampValue': '2021-01-26T23:00:00Z'},
            'created': {'timestampValue': '2021-01-22T11:42:18.710Z'},
            'departureDate': {'timestampValue': '2021-01-30T22:59:59.999Z'},
            'kind': {'stringValue': 'COLIVING'},
            'numberOfNights': {'integerValue': '3'},
            'status': {'stringValue': 'PENDING_REVIEW'}
        }
    }
    context = DotMap({
      "resource": "projects/trentiemeciel/databases/(default)/documents/pax/auth0|5ff87d92a54dd0006f957407/requests/HyynoZhPhxJnEyQBMdDU"
    })
    from_firestore(data, context)
