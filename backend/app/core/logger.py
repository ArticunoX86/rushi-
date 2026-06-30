import logging
import sys

# Create Logger
logger = logging.getLogger("AICallingAgent")

logger.setLevel(logging.INFO)

# Console Output
console_handler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)