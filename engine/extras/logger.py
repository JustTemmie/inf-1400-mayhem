"""
This module just initializes the logging module with some pre-defined paramaters
Authors: JustTemmie (i'll replace names at handin)
"""

# this file should only be imported once, preferably in Game.py or smth

from engine.extras.command_line_arguments import args

import config

import logging
import os
import datetime

if not os.path.isdir("logs"):
    os.mkdir("logs")

log_level = config.LOG_LEVEL

if args.log_level:
    log_level = args.log_level


logging.basicConfig(level=log_level,
                    format="%(levelname)s - %(message)s",
                    filename=f"logs/{datetime.datetime.now()}.log")

logging.info("Info logging enabled")
logging.debug("Debug logging enabled")
