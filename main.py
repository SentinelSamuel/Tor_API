#!/usr/bin/env python3

"""Entry point."""

import argparse

from Tor_Project.api_tor import get_exit_nodes_ip

#from IoC_Project.s1_api_ioc import

# Parameters
parser = argparse.ArgumentParser(description='Retrieves Tor exit nodes ip address using Tor DNSBL API')
parser.add_argument('-E', '--export', action="store", type=str, required=False, help='Export results in your file')
parser.add_argument('-s', '--silent' , action="store_true", required=False, help='Display nothing but the result')
parser.add_argument('--debug', action="store_true", required=False, help='Get all info')
args = parser.parse_args()

def main():
    '''
        Does everything
    '''
    tabl_exit_nodes_ip = get_exit_nodes_ip(args.export, args.silent, args.debug)


if __name__ == "__main__":
    main()
