import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--debug", type=int, help="boolean, whether to log debug info or not"
)

args = parser.parse_args()
