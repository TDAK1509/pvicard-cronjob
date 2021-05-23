import requests

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
        request_body = request.json()
        return (
            request.status_code,
            request_body.get("message", "Empty error message."),
        )
