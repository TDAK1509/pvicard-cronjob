import os

from http import HTTPStatus
from models.lazada.logger import LazadaLogger
from models.lazada.lazada import Lazada as LazadaApi
from models.lazada.pvicard import PviCard


LAZADA_APP_KEY = os.environ.get("LAZADA_APP_KEY", "dummy_api_key")
LAZADA_APP_SECRET = os.environ.get("LAZADA_APP_SECRET", "dummy_api_secret")
PVICARD_API_TOKEN = os.environ.get(
    "PVICARD_API_TOKEN", "7ff2ff9939634a3c69b312fbdba467c214714bc9"
)

logger = LazadaLogger().get_logger(__name__)


def main():
    try:
        # lazada = LazadaApi(LAZADA_APP_KEY, LAZADA_APP_SECRET)
        # pending_orders = lazada.get_pending_orders()
        pending_orders = [
            {
                "email": "dbcgdhh@gmail.com",
                "order_number": "21",
                "code_prefix_list_comma_separated": "EM1",
            },
            {
                "email": "dbcgdhh@gmail.com",
                "order_number": "22",
                "code_prefix_list_comma_separated": "EM2,EM1",
            },
        ]

        pvi_card = PviCard(PVICARD_API_TOKEN)

        for order in pending_orders:
            response = pvi_card.sync_orders(**order)
            handle_sync_order_response(order["order_number"], response)
    except Exception as e:
        logger.exception(str(e))


def handle_sync_order_response(order_number: str, request):
    status_code = request.status_code

    if status_code == HTTPStatus.OK:
        logger.info(f"Order {order_number} is successfully processed.")
    elif status_code == HTTPStatus.UNAUTHORIZED:
        logger.error(
            f"Order {order_number} failed with code {status_code}. Invalid API TOKEN"
        )
    elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        logger.error(
            f"Order {order_number} failed with code {status_code}. pvicard server error."
        )
    else:
        request_body = request.json()
        message = request_body.get("message", "Empty error message.")
        logger.error(f"Order {order_number} failed with code {status_code}. {message}")


if __name__ == "__main__":
    main()
