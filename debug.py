import logging
import threading
import time

# Define new log levels
SUCCESS_LEVEL_NUM = 25
LOADING_LEVEL_NUM = 15

logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")
logging.addLevelName(LOADING_LEVEL_NUM, "LOADING")

# Existing success method


def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)


logging.Logger.success = success

# New loading method


# New loading method
def loading(self, message, *args, **kws):
    def blink_dots():
        i = 0
        while getattr(threading.currentThread(), "do_run", True):
            record = logging.LogRecord(name=self.name, level=logging.INFO, pathname=None, lineno=None, msg=message + '.' * i, args=args, exc_info=None)
            formatted_message = self.handlers[0].formatter.format(record)
            print(f"\r{formatted_message}", end='', flush=True)
            time.sleep(1)
            i = (i + 1) % 4

    thread = threading.Thread(target=blink_dots)
    thread.do_run = True
    thread.start()
    return thread


logging.Logger.loading = loading


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'WARNING': '33',  # Yellow
        'INFO': '37',     # White
        'DEBUG': '36',    # Cyan
        'CRITICAL': '41',  # Red
        'ERROR': '31',    # Red
        'SUCCESS': '32',  # Green
        'LOADING': '37'   # White (same as INFO)
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '37')  # Default to white
        return f"\033[1;{log_color}m{super().format(record)}\033[1;m"


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Apply colored formatter
logger = logging.getLogger()
for handler in logger.handlers:
    handler.setFormatter(ColoredFormatter(handler.formatter._fmt))


class Log:
    _loading_thread = None  # Class attribute to store the loading thread
    _last_loading_message = None  # Class attribute to store the last loading message

    @staticmethod
    def _stop_loading():
        if Log._loading_thread:
            Log._loading_thread.do_run = False
            Log._loading_thread.join()
            print(f"\r{' ' * 100}", end='', flush=True)  # Clear the line
            record = logging.LogRecord(name=logger.name, level=logging.INFO, pathname=None, lineno=None, msg=Log._last_loading_message, args=(), exc_info=None)
            formatted_message = logger.handlers[0].formatter.format(record)
            print(f"\r{formatted_message}", end='', flush=True)  # Use the original message without dots
            print("", end='\n', flush=True)  # Explicitly move to the next line
            Log._loading_thread = None

    @staticmethod
    def loading(message):
        Log._stop_loading()  # Stop any existing loading thread
        Log._last_loading_message = message  # Store the original message
        logger = logging.getLogger()
        Log._loading_thread = logger.loading(message)

    @staticmethod
    def debug(message):
        Log._stop_loading()
        logging.debug(message)

    @staticmethod
    def info(message):
        Log._stop_loading()
        logging.info(message)

    @staticmethod
    def error(message):
        Log._stop_loading()
        logging.error(message)

    @staticmethod
    def success(message):
        Log._stop_loading()
        logging.getLogger().success(message)

    @staticmethod
    def warn(message):
        Log._stop_loading()
        logging.warning(message)

    @staticmethod
    def critical(message):
        Log._stop_loading()
        logging.critical(message)
