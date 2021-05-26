import requests


class PviCard:
    def __init__(self, api_token: str):
        self.__api_token = api_token

    def sync_orders(
        self,
        email: str,
        order_number: str,
        code_prefix_list_comma_separated: str,
    ):
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
        return response
