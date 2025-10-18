import logging
from colorama import init, Fore, Style

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)
        formatted = super().format(record)
        return f"{color}{formatted}{Style.RESET_ALL}"


handler = logging.StreamHandler()
handler.setFormatter(
    ColoredFormatter("%(asctime)s [%(levelname)s] %(message)s")
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

if __name__ == '__main__':
    logger.info("Program started ")
    logger.warning("Its a warning ")
    logger.error("Something went wrong ")
