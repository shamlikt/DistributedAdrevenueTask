import os
import argparse

from dask.distributed import Client
from utils import setup_logger
from transformer import Transformer
logger = setup_logger('Admarketplace_app')
SERVER_ADDRESS = os.getenv('DASK_ADDRESS', 'tcp://schedulerNode:8786')


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-a', '--ads', action="store", default="", required=True,
                       help='''ads path file''')

    parse.add_argument('-p', '--publisher', action="store", default="config", required=True,
                       help='''publisher file''')

    parse.add_argument('-o', '--output', action="store", default="", required=True,
                       help='''output file''')

    parse.add_argument('-d', '--date', action="store", default="", required=True,
                       help='''output file''')

    parse.add_argument('-c', '--cluster', action="store_true", default="",
                       help='''run time''')
    return parse.parse_args()



def main():
    args = parse_args()
    if args.cluster:
        logger.info('Selected Cluster run option')
        if not SERVER_ADDRESS:
            raise ValueError('Could not find Server existing')
        client = Client(SERVER_ADDRESS)
    else:
        logger.info('Selected local run option')
        client = None

    transformer = Transformer(logger, client)
    transformer.transform_data(args.publisher, args.ads, args.date, args.output)
    logger.info('Exiting')
    
if __name__ == '__main__':
    main()

    
