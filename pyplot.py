"""Module to bundle plotting scripts"""

import argparse


def parse_arguments():
    """Argument Parser, providing available scripts"""
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
