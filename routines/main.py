## routines/main.py
import logging
from utils.log_setup import setup_logging
from SubRoutines import SubRoutineSetView5

def main():
    # Restante do código
    setup_logging()
    logging.debug("Log Test - DEBUG")
    logging.info("Log Test - INFO")
    logging.warning("Log Test - WARNING")
    logging.error("Log Test - ERROR")
    logging.critical("Log Test - CRITICAL")

SubRoutineSetView5()