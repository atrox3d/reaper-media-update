import logging
from pathlib import Path

def setup_logging(
                    root_level: int|str =logging.INFO,
                    format: str='%(levelname)5s | %(message)s'
                ) -> logging.Logger:
    LOGFILE = str(Path(__file__).parent / Path(__file__).stem) + '.log'
    handlers = [
        logging.FileHandler(LOGFILE, mode='w'),
        logging.StreamHandler()
    ]
    logging.basicConfig(level=root_level, format=format, handlers=handlers)

def get_logger(level: int|str =logging.INFO) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    return logger
