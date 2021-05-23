import os
from models.lazada.logger import LazadaLogger
from models.lazada.lazada import Lazada as LazadaApi


APP_KEY = os.environ.get("LAZADA_APP_KEY", "dummy_api_key")
APP_SECRET = os.environ.get("LAZADA_APP_SECRET", "dummy_api_secret")

logger = LazadaLogger().get_logger("lazada")


def main():
    lazada = LazadaApi(APP_KEY, APP_SECRET)
    pending_orders = lazada.get_pending_orders()
    print(pending_orders)


if __name__ == "__main__":
    main()
