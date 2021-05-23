import os

from http import HTTPStatus
from models.lazada.logger import LazadaLogger
from models.lazada.lazada import Lazada as LazadaApi
from models.lazada.pvicard import PviCard


LAZADA_APP_KEY = os.environ.get("LAZADA_APP_KEY", "dummy_api_key")
LAZADA_APP_SECRET = os.environ.get("LAZADA_APP_SECRET", "dummy_api_secret")
PVICARD_API_TOKEN = os.environ.get(
    "PVICARD_API_TOKEN", "7ff2ff9939634a3c69b312fbdba467c214714bc91"
)

logger = LazadaLogger().get_logger(__name__)


def main():
    try:
        # lazada = LazadaApi(LAZADA_APP_KEY, LAZADA_APP_SECRET)
        # pending_orders = lazada.get_pending_orders()
        pending_orders = [
            {
                "email": "dbcgdhh@gmail.com",
                "phone": "123456",
                "order_number": "21",
                "code_prefix": "C41",
                "customer_name": "Khuong",
            },
        ]

        pvi_card = PviCard(PVICARD_API_TOKEN)

        for order in pending_orders:
            response = pvi_card.sync_orders(**order)
            handle_sync_order_response(order["order_number"], response)
    except Exception as e:
        logger.exception(str(e))


def handle_sync_order_response(order_number: str, request):
    request_body = request.json()
    status_code = request.status_code
    message = request_body.get("message", "Empty error message.")

    if status_code == HTTPStatus.OK:
        logger.info(f"Order {order_number} is successfully processed.")
    else:
        logger.error(
            f"Order {order_number} failed with code {status_code}. Error message: {message}"
        )


if __name__ == "__main__":
    main()
