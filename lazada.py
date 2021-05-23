import os
import requests

from http import HTTPStatus
from models.lazada.logger import LazadaLogger
from models.lazada.lazada import Lazada as LazadaApi


LAZADA_APP_KEY = os.environ.get("LAZADA_APP_KEY", "dummy_api_key")
LAZADA_APP_SECRET = os.environ.get("LAZADA_APP_SECRET", "dummy_api_secret")
PVICARD_API_TOKEN = os.environ.get(
    "PVICARD_API_TOKEN", "7ff2ff9939634a3c69b312fbdba467c214714bc9"
)

logger = LazadaLogger().get_logger("lazada")


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

        for order in pending_orders:
            status_code, message = sync_orders(PVICARD_API_TOKEN, **order)
            order_number = order["order_number"]

            if status_code == HTTPStatus.OK:
                logger.info(f"Order {order_number} is successfully processed.")
            else:
                logger.error(
                    f"Order {order_number} failed with code {status_code}. Error message: {message}"
                )
    except Exception as e:
        logger.exception(str(e))


def sync_orders(
    token: str,
    email: str,
    phone: str,
    order_number: str,
    code_prefix: str,
    customer_name: str,
):
    request_url = "https://pvicard.com/api/merchant/sync-orders/lazada/"

    request_data = {
        "email": email,
        "phone": phone,
        "order_number": order_number,
        "code_prefix": code_prefix,
        "customer_name": customer_name,
    }
    request = requests.post(
        request_url,
        headers={"Authorization": f"Token {token}"},
        data=request_data,
    )
    request_body = request.json()
    return (request.status_code, request_body.get("message", "Empty error message."))


if __name__ == "__main__":
    main()
