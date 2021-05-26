import requests

from models.lazada.logger import LazadaLogger


logger = LazadaLogger().get_logger(__name__)


class PviCard:
    def __init__(self, api_token: str):
        self.__api_token = api_token

    def sync_orders(
        self,
        email: str,
        order_number: str,
        code_prefix_list_comma_separated: str,
    ):
        logger.info(
            f"Syncing order {order_number} to pvicard.com server, code prefix list: {code_prefix_list_comma_separated}"
        )
        request_url = "https://pvicard.com/api/merchant/sync-orders/api_lazada/"

        request_data = {
            "email": email,
            "order_number": order_number,
            "code_prefix_list": code_prefix_list_comma_separated,
        }
        response = requests.post(
            request_url,
            headers={"Authorization": f"Token {self.__api_token}"},
            data=request_data,
        )
        logger.info(
            f"Done syncing order {order_number} to pvicard.com server, code prefix list: {code_prefix_list_comma_separated}"
        )
        return response
