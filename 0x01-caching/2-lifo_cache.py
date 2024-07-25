#!/usr/bin/python3
""" Log parsing script """

import sys
import signal

# Initialize global variables
file_size = 0
status_codes = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0


def print_stats():
    """ Function to print the statistics """
    print("File size: {}".format(file_size))
    for code in sorted(status_codes):
        if status_codes[code] > 0:
            print("{}: {}".format(code, status_codes[code]))


def signal_handler(sig, frame):
    """ Signal handler to print stats on keyboard interruption """
    print_stats()
    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        parts = line.split()
        if len(parts) > 6:
            try:
                status_code = int(parts[-2])
                size = int(parts[-1])
                if status_code in status_codes:
                    status_codes[status_code] += 1
                file_size += size
                line_count += 1
            except ValueError:
                continue

        if line_count % 10 == 0:
            print_stats()
except KeyboardInterrupt:
    print_stats()
    raise
