"""
This module just lets the program take in command line arguments
Authors: JustTemmie (i'll replace names at handin)
"""

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--log-level", type=int, help="Overwrite the log level defined in the config file"
)

args = parser.parse_args()
