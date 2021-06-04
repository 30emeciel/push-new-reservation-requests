from datetime import datetime, timezone, timedelta

import dotenv
import pytest
from box import Box
from core import firestore_client
from google.cloud.firestore_v1 import Client, DocumentSnapshot, DocumentReference
from mockito import mock

PARIS_TZ = timezone(timedelta(hours=2))


@pytest.fixture(autouse=True)
def setup():
    dotenv.load_dotenv()


@pytest.fixture(autouse=False)
def db(when):
    ret = mock(Client)
    when(firestore_client).db().thenReturn(ret)
    return ret


def test_push_new_reservation_request_to_slack(when, db):


    import main

    doc_path = 'pax/auth0|5ff87d92a54dd0006f957407/requests/MPWWj2CgAORm3AQS7Vj7'

    pax_ref_mock = mock(spec=DocumentReference)
    pax_doc_mock = mock({"exists": True}, spec=DocumentSnapshot)
    pax_data_mock = {
        "name": "Name",
    }
    reservation_ref_mock = mock({"parent": Box({"parent": pax_ref_mock})}, spec=DocumentReference)
    reservation_doc_mock = mock({"exists": True}, spec=DocumentSnapshot)
    reservation_data_mock = {
        "state": "PENDING_REVIEW",
        "kind": "COLIVING",
        "arrival_date": datetime(2022, 2, 20, tzinfo=PARIS_TZ),
        "departure_date": datetime(2022, 2, 26, tzinfo=PARIS_TZ),
        "number_of_nights": 7,
    }
    when(db).document(doc_path).thenReturn(reservation_ref_mock)
    when(pax_ref_mock).get().thenReturn(pax_doc_mock)
    when(pax_doc_mock).to_dict().thenReturn(pax_data_mock)
    when(reservation_ref_mock).get().thenReturn(reservation_doc_mock)
    when(reservation_doc_mock).to_dict().thenReturn(reservation_data_mock)
    event = {
        "state": "PENDING_REVIEW"
    }

    main.push_new_reservation_request_to_slack(doc_path=doc_path, event=Box(event))

