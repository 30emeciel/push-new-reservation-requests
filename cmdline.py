import logging
from dotmap import DotMap

log = logging.getLogger(__name__)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    # export GOOGLE_APPLICATION_CREDENTIALS="trentiemeciel.json"
    # get the token using postman
    import main
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
    path = '/pax/auth0|5ff87d92a54dd0006f957407/requests/aw6h5SkfLRpbdqboR9J1'
    context = DotMap({
        "resource": f'projects/trentiemeciel/databases/(default)/documents{path}'
    })
    main.from_firestore(data, context)
