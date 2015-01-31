"""Tool to transform a json file into a png image of a graph using blockdiag.
"""

import json
import os
import subprocess
import tempfile

from replace_stdout import capture


ORIENTATION_LINE = "blockdiag {{ orientation = {}"
GRAPH_LINE = "   {} -> {};"
END_LINE = "}"


def _print_blockdiag(tree, parent=None, orientation='landscape'):
    """Writes the blockdiag information to file.

    Parameters
    ----------
    tree : dict, string
        The information to be written to file.
    parent : string, optional
        The parent of the current key.
    orientation : string, optional
        The orientation that should be used in the blockdiag.
    """

    if not parent:
        print ORIENTATION_LINE.format(orientation)
        
    if not isinstance(tree, basestring):
        for key in tree:
            if parent:
                print GRAPH_LINE.format(parent, key)
            try:
                _print_blockdiag(tree[key], key)
            except TypeError:
                print GRAPH_LINE.format(parent, key)

        if not parent:
            print END_LINE
    else:
        if tree == "":
            tree = "None"
        print GRAPH_LINE.format(parent, tree)


def to_blockdiag(graph_dict, output_file):
    """Converts a graph to a blockdiag file.

    Parameters
    ----------
    graph_dict : dict
        The graph to be turned into a blockdiag file.
    output_file : file-like
        The stream to which the graph should be written.
    """

    with capture(output_file):
        _print_blockdiag(graph_dict)


def blockdiag_to_png(input_file):
    """Transforms a blockdiag file to a png file.

    Parameters
    ----------
    input_file : string
        The name of the blockdiag file.
    """

    subprocess.check_call(["blockdiag", input_file])


def display_image(image_name):
    """Displays an image.

    Parameters
    ----------
    image_name : string
        The name of the image file.
    """
    subprocess.check_call([image_name], shell=True)


def json_to_png(input_file, image_name, keep_diag_file=False, display=True):
    """Full process of converting a json file of a graph into an image.

    Parameters
    ----------
    input_file : string
        The name of the json file.
    image_name : string
        The desired name of the image file.
    keep_diag_file : bool, optional
        Whether or not the intermediate .diag file should be kept.  Defaults to
        False.
    display : bool, optional
        Whether or not the resulting image should be immediately displayed.
        Defaults to True.
    """

    with open(input_file, 'r') as json_file:
        graph_dict = json.load(json_file)

    if not keep_diag_file:
        f = tempfile.NamedTemporaryFile(mode='w', suffix='diag')
    else:
        f = open("{}.diag".format(input_file.name), 'w')

    to_blockdiag(graph_dict, f)
    blockdiag_to_png(f.name)
    os.rename(f.name, image_name)
    if display:
        display_image(image_name)


if __name__ == '__main__':
    import argparse

    USAGE = "$ python to_blockdiag.py output_file [, input_file]"

    parser = argparse.ArgumentParser(description= \
        "Converts a json file to a png image using blockdiag.\nUsage: {}"
            .format(USAGE))
    parser.add_argument('file', metavar='F', type=str, nargs='1',
                        help="The json file to be transformed.")
    parser.add_argument('-o', '--out_file', default=False, action='store_true',
                        help="Use if the intermediate file should be saved.")
    parser.add_argument('-i', '--image_file', default=None,
                        help="The name of the image file")
    parser.add_argument('-d', '--display', default=False, action='store_true',
                        help="Use if you would like to display the image.")

    args = parser.parse_args()
    if args.image_file:
        image_name=args.image_file
    else:
        image_name=args.file.partition('.')[0]

    json_to_png(args.file, image_name,
                keep_diag_file=args.out_file, display=args.display)