# this file should only be imported once, preferably in Game.py or smth
import logging

from engine.extras.command_line_arguments import args
from config import LOG_DEBUG_EVENTS

log_level = logging.INFO

if args.debug or LOG_DEBUG_EVENTS:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level, format="%(levelname)s - %(message)s")

logging.debug("Debug logging enabled")