"""Converts a space delimited file to a comma delimited file."""

import csv
import sys


def space_delim_to_comma_delim(space_delim, comma_delim):
    """Converts a space delimited file to a comma delimited file.

    Parameters
    ----------
    space_delim : string
        The filename of the space delimited file to be converted.
    comma_delim : string
        The filename of the comma delimited file to be written to.
    """

    buffer_strings = []

    with open(space_delim, "r") as f:
        for line in f:
            buffer_strings.append(line.split())

    with open(comma_delim, "wb") as f:
        my_writer = csv.writer(f)
        for buffer_string in buffer_strings:
            my_writer.writerow(buffer_string)


if __name__ == '__main__':
    space_delim_to_comma_delim(sys.argv[1], sys.argv[2])
