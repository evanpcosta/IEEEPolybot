"""Command line interface for polybot"""

import logging
import os
from argparse import ArgumentParser, Namespace

import requests
from preprocess_functions.dichroic_pre import dichroic_pre
from preprocess_functions.electrical_pre import electrical_pre
import pandas as pd
import cv2


from polybot.version import __version__

logger = logging.getLogger(__name__)


def upload(args: Namespace):
    """Upload a file"""

    # Read in the file
    with open(args.file, 'rb') as fp:
        content = fp.read()
    logger.info(f'Read in a {len(content) / 1024: .2f} kB file')

    # Make the upload package
    url = f'{args.host_url}/ingest'
    logger.info(f'Uploading file to {url}')
    result = requests.post(url, data={'name': args.name}, files={'file': (args.file, content)})
    logger.info(f'Request status: {result.status_code}')
    if result.status_code == 200:
        print(result.json())
    else:
        print(f'Failed with a status: {result.json()}')

def preprocess(args: Namespace):
    """ Preprocess data in the folder and add to master csv"""

    # finds the name of the experiment based on the directory name
    exp_name = args.dirpath.split("/")[-1]

    if not os.path.isdir(args.dirpath):
        logger.info("Directory",args.dirpath, "not available")
        return

    json = {}
    for filename in os.listdir(args.dirpath):
        name = filename.split(".")[0]
        print(name)

        # some way to distinguish between the 2 types of files
        # needs to be changed if the naming scheme changes
        if "dichroic_data" in name:
            # finds the name of all samples and their dichroic ratios
            ratio_names, ratios = dichroic_pre(os.path.join(args.dirpath, filename))
            ratio_tuples = list(zip(ratio_names, ratios))

            # loads all of the ratio information into a database
            for ii in range(len(ratio_names)):
                json[ratio_names[ii]] = {"dichroic_ratio":ratios[ii]}
        elif "electrical_data" in name:
            # for every electrical datafile
            for data_name in os.listdir(os.path.join(args.dirpath, filename)):
                sample_name = data_name.split(".")[0]
                # get the m and b
                m, b = electrical_pre(os.path.join(args.dirpath, filename+"/"+data_name))

                # store it in the db
                if sample_name not in json:
                    json[sample_name] = {}
                json[sample_name]["m"] = m
                json[sample_name]["b"] = b
        elif "image" in name:
            # create image classifier here
            # 0.02 for image for variance of greyscale image
            pass
        else:
            logger.info("File name " +name+" not found")


    db = pd.DataFrame.from_dict(json)
    db.to_csv("preprocessed/"+exp_name+".csv", encoding = "utf-8", date_format="%s")

    # with open(args.file, 'rb') as fp:
    #     content = fp.read()
    # logger.info(f'Read in a {len(content) / 1024: .2f} kB file')


def create_parser() -> ArgumentParser:
    """Create the argument parser for the CLI tool"""

    parser = ArgumentParser()
    parser.add_argument('--version', action='store_true', help='Print version number and exit')
    parser.add_argument('--verbose', action='store_true', help='Turn on logging')
    parser.add_argument('--host', help='URL of polybot service', type=str, default='localhost')
    parser.add_argument('--port', help='Port of polybot service', type=int, default=5000)
    sub_parser = parser.add_subparsers(title='Subcommands',
                                       help='Available subcommands for polybot')

    # Create the upload functionality
    upload_parser = sub_parser.add_parser('upload', help='Upload files to polybot')
    upload_parser.add_argument('--dry-run', action='store_true',
                               help='Ready but do not upload file')
    upload_parser.add_argument('name', help='Name of the experiment', type=str)
    upload_parser.add_argument('file', help='Path to the file to upload', type=str)
    upload_parser.set_defaults(function=upload)

    # Create preprocess functionality
    preprocess_parser = sub_parser.add_parser("preprocess", help = "Preprocess file")
    preprocess_parser.add_argument('dirpath', help = "Path of the experiment directory", type = str)
    preprocess_parser.set_defaults(function=preprocess)
    return parser


def main(args=None):
    """Run the command line interface"""

    # Make and run the parser
    parser = create_parser()
    args = parser.parse_args(args)

    # Make the logger if desired
    if args.verbose:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
    logger.info(f'Running polybot CLI app. Version: {__version__}')
    args.host_url = f'http://{args.host}:{args.port}'
    logger.info(f'Connecting to server at {args.host_url}')

    # Act on the parser
    if args.version:
        print(f'polybot version: {__version__}')
        return
    args.function(args)
