import argparse


def parse_arguments():
    """Parse arguments from command line"""
    parser = argparse.ArgumentParser(description="Process app configuration.")
    parser.add_argument(
        "--config", "-c", type=str, help="configuration file", default="config.toml"
    )
    return parser.parse_args()
