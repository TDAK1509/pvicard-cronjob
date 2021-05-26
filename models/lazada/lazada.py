import os
from lib.lazada import base as lazop


class Lazada:
    def __init__(self, app_key: str, app_secret: str):
        self.__app_key = app_key
        self.__app_secret = app_secret
        self.__access_token()

    def __get_access_token(self):
        api_url_my = "https://api.lazada.com.my/rest"
        refresh_token = os.environ.get("LAZADA_REFRESH_TOKEN")

        client = lazop.LazopClient(api_url_my, self.__app_key, self.__app_secret)
        request = lazop.LazopRequest("/auth/token/refresh")
        request.add_api_param("refresh_token", refresh_token)
        response = client.execute(request)

        if "access_token" not in response.keys():
            error_code = response["code"]
            error_message = response["message"]
            raise ValueError(f"{error_code}: {error_message}")

        self.__access_token = response["access_token"]

    def get_pending_orders(self):
        api_url_vn = "https://api.lazada.vn/rest"
        client = lazop.LazopClient(api_url_vn, self.__app_key, self.__app_secret)
        request = lazop.LazopRequest("/orders/get", "GET")

        request.add_api_param("status", "pending")
        request.add_api_param("created_after", "2021-01-01T01:00:00+07:00")
        response = client.execute(request, self.__access_token)

        return list(response["data"]["orders"])
