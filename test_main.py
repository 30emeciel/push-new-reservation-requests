from unittest import TestCase

import dotenv
from box import Box


class Test(TestCase):

    def setUp(self) -> None:
        dotenv.load_dotenv()

    def test_push_new_reservation_request_to_slack(self):
        import main
        doc_path = 'pax/auth0|5ff87d92a54dd0006f957407/requests/MPWWj2CgAORm3AQS7Vj7'
        event = {
            "state": "PENDING_REVIEW"
        }

        main.push_new_reservation_request_to_slack(doc_path=doc_path, event=Box(event))

