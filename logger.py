import logging
from pathlib import Path

LOG_PATH = Path("logs")
LOG_PATH.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_PATH / "votesecure.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("votesecure")
