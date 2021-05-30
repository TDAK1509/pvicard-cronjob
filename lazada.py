import getopt, sys

from http import HTTPStatus
from models.lazada.logger import LazadaLogger
from models.lazada.lazada import Lazada as LazadaApi
from models.lazada.pvicard import PviCard


command_line_args = sys.argv[1:]
opts, args = getopt.getopt(
    command_line_args,
    "k:s:t:rf",
    [
        "lazada-app-key=",
        "lazada-app-secret=",
        "pvicard-api-token=",
    ],
)

for key, value in opts:
    if key in ("-k", "--lazada-app-key"):
        LAZADA_APP_KEY = value
    elif key in ("-s", "--lazada-app-secret"):
        LAZADA_APP_SECRET = value
    elif key in ("-t", "--pvicard-api-token"):
        PVICARD_API_TOKEN = value


logger = LazadaLogger().get_logger(__name__)


def main():
    logger.info("\n======================\nStarting cronjob")
    try:
        pvi_card = PviCard(PVICARD_API_TOKEN)
        lazada_refresh_token = pvi_card.fetch_refresh_token()

        lazada = LazadaApi(LAZADA_APP_KEY, LAZADA_APP_SECRET, lazada_refresh_token)
        pending_orders = lazada.get_pending_orders_details()

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


def handle_sync_order_response(order_number: str, response):
    status_code = response.status_code

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
        request_body = response.json()
        message = request_body.get("message", "Empty error message.")
        raise Exception(
            f"Order {order_number} failed with code {status_code}. {message}"
        )


if __name__ == "__main__":
    main()
