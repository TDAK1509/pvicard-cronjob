from models.lazada.logger import LazadaLogger
from models.lazada.lazada import Lazada as LazadaApi

logger = LazadaLogger().get_logger("lazada")


def main():
    lazada = LazadaApi()
    pending_orders = lazada.get_pending_orders()
    print(pending_orders)


if __name__ == "__main__":
    main()
