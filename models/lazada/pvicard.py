import requests


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

        request_data = {
            "email": email,
            "phone": phone,
            "order_number": order_number,
            "code_prefix": code_prefix,
            "customer_name": customer_name,
        }
        response = requests.post(
            request_url,
            headers={"Authorization": f"Token {self.__api_token}"},
            data=request_data,
        )
        return response
