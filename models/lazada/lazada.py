import os
from lib.lazada import base as lazop
from models.lazada.logger import LazadaLogger


logger = LazadaLogger().get_logger(__name__)


class Lazada:
    def __init__(self, app_key: str, app_secret: str):
        self.__api_url = "https://api.lazada.vn/rest"
        self.__app_key = app_key
        self.__app_secret = app_secret
        self.__get_access_token()

    def __get_access_token(self):
        logger.info("Getting access token")
        refresh_token = os.environ.get("LAZADA_REFRESH_TOKEN")

        client = lazop.LazopClient(self.__api_url, self.__app_key, self.__app_secret)
        request = lazop.LazopRequest("/auth/token/refresh")
        request.add_api_param("refresh_token", refresh_token)
        response = client.execute(request)

        if "access_token" not in response.keys():
            error_code = response["code"]
            error_message = response["message"]
            raise ValueError(f"{error_code}: {error_message}")

        self.__access_token = response["access_token"]
        logger.info("Finish getting access token")

    def get_pending_orders_details(self):
        logger.info("Get pending order details")
        pending_order_numbers = self.__get_pending_orders()
        orders_details = []

        for order_number in pending_order_numbers:
            order_detail = self.__extract_information_from_order_number(order_number)
            orders_details.append(order_detail)
        logger.info("Finish getting pending order details")
        return orders_details

    def __get_pending_orders(self):
        logger.info("Getting pending orders from Lazada")
        client = lazop.LazopClient(self.__api_url, self.__app_key, self.__app_secret)
        request = lazop.LazopRequest("/orders/get", "GET")

        request.add_api_param("status", "pending")
        request.add_api_param("created_after", "2021-01-01T01:00:00+07:00")
        response = client.execute(request, self.__access_token)

        orders = list(response["data"]["orders"])
        order_numbers = [order["order_number"] for order in orders]
        logger.info("Finish getting pending orders from Lazada")

        return order_numbers

    def __extract_information_from_order_number(self, order_number: str):
        logger.info(f"Extracting information from order {order_number}")
        order_items = self.__get_order_items(order_number)
        email = order_items[0]["digital_delivery_info"]
        code_prefix_list = [item["sku"][0:3] for item in order_items]
        order_detail = {
            "email": email,
            "order_number": order_number,
            "code_prefix_list_comma_separated": ",".join(code_prefix_list),
        }
        logger.info(f"Finish extracting information from order {order_number}")
        return order_detail

    def __get_order_items(self, order_number: str):
        logger.info(f"Making API request to Lazada for order {order_number}")
        client = lazop.LazopClient(self.__api_url, self.__app_key, self.__app_secret)
        request = lazop.LazopRequest("/order/items/get", "GET")

        request.add_api_param("order_id", order_number)
        response = client.execute(request, self.__access_token)
        logger.info(f"Finish making API request to Lazada for order {order_number}")
        return list(response["data"])
