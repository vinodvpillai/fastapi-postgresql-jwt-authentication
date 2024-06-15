import logging
import sys

# Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Log format
fmt = logging.Formatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
)

# Create handlers - Standard output & File
stdoutHandler = logging.StreamHandler(stream=sys.stdout)
msgHandler = logging.FileHandler("msg.log")

# Set the log format on each handler
stdoutHandler.setFormatter(fmt)
msgHandler.setFormatter(fmt)

# Set the log levels on the handlers
stdoutHandler.setLevel(logging.INFO)
msgHandler.setLevel(logging.INFO)

# Add each handler to the Logger object
logger.handlers = [stdoutHandler, msgHandler]