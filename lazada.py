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
        lazada = LazadaApi(LAZADA_APP_KEY, LAZADA_APP_SECRET)
        pending_orders = lazada.get_pending_orders_details()

        pvi_card = PviCard(PVICARD_API_TOKEN)

        for order in pending_orders:
            order_number = order["order_number"]
            response = pvi_card.sync_orders(
                email=order["email"],
                order_number=order_number,
                code_prefix_list_comma_separated=order[
                    "code_prefix_list_comma_separated"
                ],
            )
            handle_sync_order_response(order_number, response)
            lazada.set_order_status_ready_to_ship(order_number, order["order_item_ids"])

        logger.info(f"Task DONE for orders {pending_orders}")
    except Exception as e:
        logger.exception(str(e))


def handle_sync_order_response(order_number: str, request):
    status_code = request.status_code

    if status_code == HTTPStatus.OK:
        logger.info(f"Order {order_number} is successfully processed.")
    elif status_code == HTTPStatus.UNAUTHORIZED:
        raise Exception(
            f"Order {order_number} failed with code {status_code}. Invalid API TOKEN"
        )
    elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        raise Exception(
            f"Order {order_number} failed with code {status_code}. pvicard server error."
        )
    else:
        request_body = request.json()
        message = request_body.get("message", "Empty error message.")
        raise Exception(
            f"Order {order_number} failed with code {status_code}. {message}"
        )


if __name__ == "__main__":
    main()
