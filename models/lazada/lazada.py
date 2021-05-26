import os
from lib.lazada import base as lazop


class Lazada:
    def __init__(self, app_key: str, app_secret: str):
        self.__api_url = "https://api.lazada.vn/rest"
        self.__app_key = app_key
        self.__app_secret = app_secret
        # self.__get_access_token()

    def __get_access_token(self):
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

    def get_pending_orders_details(self):
        pending_order_numbers = self.__get_pending_orders()
        orders_details = []

        for order_number in pending_order_numbers:
            order_detail = self.__extract_information_from_order_number(order_number)
            orders_details.append(order_detail)
        return orders_details

    def __extract_information_from_order_number(self, order_number: str):
        order_items = self.__get_order_items(order_number)
        email = order_items[0]["digital_delivery_info"]
        code_prefix_list = [item["sku"][0:3] for item in order_items]
        order_detail = {
            "email": email,
            "order_number": order_number,
            "code_prefix_list_comma_separated": ",".join(code_prefix_list),
        }
        return order_detail

    def __get_order_items(self, order_number: str):
        # client = lazop.LazopClient(self.__api_url, self.__app_key, self.__app_secret)
        # request = lazop.LazopRequest("/order/items/get", "GET")

        # request.add_api_param("order_id", order_number)
        # response = client.execute(request, self.__access_token)
        response = {
            "data": [
                {
                    "tax_amount": 0.00,
                    "reason": "",
                    "sla_time_stamp": "2021-05-27T23:59:59+07:00",
                    "purchase_order_id": "",
                    "voucher_seller": 0,
                    "voucher_code_seller": "",
                    "voucher_code": "",
                    "package_id": "",
                    "variation": "",
                    "voucher_code_platform": "",
                    "purchase_order_number": "",
                    "sku": "C416535254-1621475329737-0",
                    "invoice_number": "25",
                    "order_type": "Normal",
                    "cancel_return_initiator": "null-null",
                    "shop_sku": "1306535254_VNAMZ-5058631360",
                    "is_reroute": 0,
                    "stage_pay_status": "",
                    "tracking_code_pre": "",
                    "order_item_id": 288480920219609,
                    "shop_id": "The Phong",
                    "order_flag": "NORMAL",
                    "is_fbl": 0,
                    "name": "Toàn Quốc [E-Voucher] Bảo Hiểm Bắt Buộc Trách Nhiệm Dân Sự -Xe Mô Tô 2 bánh trên 50 cc - 1 năm",
                    "delivery_option_sof": 0,
                    "order_id": 288480920119609,
                    "status": "delivered",
                    "paid_price": 66000.00,
                    "product_main_image": "https://vn-live.slatic.net/p/mdc/74e42d6f6450f16e72a0a8df32d46b92.jpg",
                    "voucher_platform": 0,
                    "product_detail_url": "https://www.lazada.vn/products/i1306535254-s5058631360.html?urlFlag=true&mp=1",
                    "promised_shipping_time": "",
                    "warehouse_code": "dropshipping",
                    "shipping_type": "Dropshipping",
                    "created_at": "2021-05-25 14:02:38 +0700",
                    "shipping_fee_discount_platform": 0,
                    "wallet_credits": 0,
                    "updated_at": "2021-05-25 14:58:24 +0700",
                    "currency": "VND",
                    "shipping_provider_type": "digital",
                    "shipping_fee_original": 0.00,
                    "is_digital": 1,
                    "item_price": 66000.00,
                    "shipping_service_cost": 0,
                    "tracking_code": "",
                    "shipping_fee_discount_seller": 0,
                    "shipping_amount": 0.00,
                    "reason_detail": "",
                    "return_status": "",
                    "shipment_provider": "",
                    "voucher_amount": 0,
                    "digital_delivery_info": "dbcgdhh@gmail.com",
                    "extra_attributes": "",
                },
                {
                    "tax_amount": 0.00,
                    "reason": "",
                    "sla_time_stamp": "2021-05-27T23:59:59+07:00",
                    "purchase_order_id": "",
                    "voucher_seller": 0,
                    "voucher_code_seller": "",
                    "voucher_code": "",
                    "package_id": "",
                    "variation": "",
                    "voucher_code_platform": "",
                    "purchase_order_number": "",
                    "sku": "C416535254-1621475329737-0",
                    "invoice_number": "25",
                    "order_type": "Normal",
                    "cancel_return_initiator": "null-null",
                    "shop_sku": "116535254_VNAMZ-5058631360",
                    "is_reroute": 0,
                    "stage_pay_status": "",
                    "tracking_code_pre": "",
                    "order_item_id": 288480920219609,
                    "shop_id": "The Phong",
                    "order_flag": "NORMAL",
                    "is_fbl": 0,
                    "name": "Toàn Quốc [E-Voucher] Bảo Hiểm Bắt Buộc Trách Nhiệm Dân Sự -Xe Mô Tô 2 bánh trên 50 cc - 1 năm",
                    "delivery_option_sof": 0,
                    "order_id": 288480920119609,
                    "status": "delivered",
                    "paid_price": 66000.00,
                    "product_main_image": "https://vn-live.slatic.net/p/mdc/74e42d6f6450f16e72a0a8df32d46b92.jpg",
                    "voucher_platform": 0,
                    "product_detail_url": "https://www.lazada.vn/products/i1306535254-s5058631360.html?urlFlag=true&mp=1",
                    "promised_shipping_time": "",
                    "warehouse_code": "dropshipping",
                    "shipping_type": "Dropshipping",
                    "created_at": "2021-05-25 14:02:38 +0700",
                    "shipping_fee_discount_platform": 0,
                    "wallet_credits": 0,
                    "updated_at": "2021-05-25 14:58:24 +0700",
                    "currency": "VND",
                    "shipping_provider_type": "digital",
                    "shipping_fee_original": 0.00,
                    "is_digital": 1,
                    "item_price": 66000.00,
                    "shipping_service_cost": 0,
                    "tracking_code": "",
                    "shipping_fee_discount_seller": 0,
                    "shipping_amount": 0.00,
                    "reason_detail": "",
                    "return_status": "",
                    "shipment_provider": "",
                    "voucher_amount": 0,
                    "digital_delivery_info": "dbcgdhh@gmail.com",
                    "extra_attributes": "",
                },
            ],
            "code": "0",
            "request_id": "0b1187a316220310876901323",
        }
        return list(response["data"])

    def __get_pending_orders(self):
        return ["288480920119609"]
        client = lazop.LazopClient(self.__api_url, self.__app_key, self.__app_secret)
        request = lazop.LazopRequest("/orders/get", "GET")

        request.add_api_param("status", "pending")
        request.add_api_param("created_after", "2021-01-01T01:00:00+07:00")
        response = client.execute(request, self.__access_token)

        orders = list(response["data"]["orders"])
        order_numbers = [order["order_number"] for order in orders]

        return order_numbers
