import os
from lib.lazada import base as lazop


class Lazada:
    __APP_KEY = os.environ.get("LAZADA_APP_KEY", "dummy_api_key")
    __APP_SECRET = os.environ.get("LAZADA_APP_SECRET", "dummy_api_secret")

    def __get_access_token(self):
        api_url_my = "https://api.lazada.com.my/rest"
        refresh_token = os.environ.get("LAZADA_REFRESH_TOKEN")

        client = lazop.LazopClient(api_url_my, self.__APP_KEY, self.__APP_SECRET)
        request = lazop.LazopRequest("/auth/token/refresh")
        request.add_api_param("refresh_token", refresh_token)
        response = client.execute(request)
        access_token = response["access_token"]
        return access_token

    def get_pending_orders(self):
        api_url_vn = "https://api.lazada.vn/rest"
        access_token = self.__get_access_token()

        client = lazop.LazopClient(api_url_vn, self.__APP_KEY, self.__APP_SECRET)
        request = lazop.LazopRequest("/orders/get", "GET")

        request.add_api_param("status", "pending")
        request.add_api_param("created_after", "2021-01-01T01:00:00+07:00")
        response = client.execute(request, access_token)

        return list(response["data"]["orders"])
