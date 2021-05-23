import requests

from http import HTTPStatus
from models.lazada.logger import LazadaLogger

logger = LazadaLogger().get_logger(__name__)


class PviCard:
    def __init__(self, api_token: str):
        self.__api_token = api_token

    def sync_orders(
        self,
        email: str,
        phone: str,
        order_number: str,
        code_prefix: str,
        customer_name: str,
    ):
        request_url = "https://pvicard.com/api/merchant/sync-orders/lazada/"
        request_url = "http://localhost:8000/api/merchant/sync-orders/test/"

        request_data = {
            "email": email,
            "phone": phone,
            "order_number": order_number,
            "code_prefix": code_prefix,
            "customer_name": customer_name,
        }
        request = requests.post(
            request_url,
            headers={"Authorization": f"Token {self.__api_token}"},
            data=request_data,
        )
        self.__handle_response(order_number, request)

    def __handle_response(self, order_number: str, request):
        request_body = request.json()
        status_code = request.status_code
        message = request_body.get("message", "Empty error message.")

        if status_code == HTTPStatus.OK:
            logger.info(f"Order {order_number} is successfully processed.")
        else:
            logger.error(
                f"Order {order_number} failed with code {status_code}. Error message: {message}"
            )
