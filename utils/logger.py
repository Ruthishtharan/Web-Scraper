import logging

def setup_logger():
    logging.basicConfig(
        filename="data/logs/app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )