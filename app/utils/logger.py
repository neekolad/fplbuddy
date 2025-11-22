import logging

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] {message}",
    datefmt="%d-%m-%Y %H:%M:%S",
    style="{"
)

logger = logging.getLogger("pl_logger")