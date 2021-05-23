import os
from lib.lazada import base as lazop
from models.lazada.logger import LazadaLogger


APP_KEY = os.environ.get("LAZADA_APP_KEY")
APP_SECRET = os.environ.get("LAZADA_APP_SECRET")


logger = LazadaLogger().get_logger("lazada")


def main():
    logger.info("testasdf")
    # access_token = get_access_token()
    # pending_orders = get_pending_orders(access_token)
    # print(pending_orders)


def get_access_token():
    api_url_my = "https://api.lazada.com.my/rest"
    refresh_token = os.environ.get("LAZADA_REFRESH_TOKEN")

    client = lazop.LazopClient(api_url_my, APP_KEY, APP_SECRET)
    request = lazop.LazopRequest("/auth/token/refresh")
    request.add_api_param("refresh_token", refresh_token)
    response = client.execute(request)
    access_token = response["access_token"]
    return access_token


def get_pending_orders(access_token: str):
    api_url_vn = "https://api.lazada.vn/rest"
    client = lazop.LazopClient(api_url_vn, APP_KEY, APP_SECRET)
    request = lazop.LazopRequest("/orders/get", "GET")
    request.add_api_param("status", "pending")
    request.add_api_param("created_after", "2021-01-01T01:00:00+07:00")
    response = client.execute(request, access_token)
    return list(response["data"]["orders"])


if __name__ == "__main__":
    main()
