#!/usr/bin/env python3

'''
Retrieves exit nodes IP addresses from Tor DNSBL API.
'''

##################### Custom API Call Python Script #####################
## This script use the Tor DNSBL API
## Created by Samuel PAGES May 15th 2023
#########################################################################

import re
import argparse
import requests
from colorama import Fore, Style
from tqdm import tqdm

# Parameters
parser = argparse.ArgumentParser(description='Retrieves Tor exit nodes ip address using Tor DNSBL API')
parser.add_argument('-E', '--export', action="store", type=str, required=False, help='Export results in your file')
parser.add_argument('-s', '--silent' , action="store_true", required=False, help='Display nothing but the result')
parser.add_argument('--debug', action="store_true", required=False, help='Get all info')
args = parser.parse_args()

def get_exit_nodes_ip(export, silent, debug):
    '''
        Retrieves Tor exit nodes ip address using Tor DNSBL API
        -E --> Export results in your file
        -s --> Export results in your file
        --debug --> Get all info
    '''
    ###########################################################################
    ######################## All tests and definitions ########################
    ###########################################################################

    # Info message
    def infotext(msg) -> str:
        '''Display informational message on console in blue

        Arguments:

        msg -- text to be printed
        '''
        print(f"{Fore.BLUE}[i] {msg} {Style.RESET_ALL}")
    # Error message
    def errortext(msg) -> str:
        '''Display success message on console in green

        Arguments:

        msg -- text to be printed
        '''
        print(f"{Fore.RED}[-] {msg} {Style.RESET_ALL}")
    # Success message
    def successtext(msg) -> str:
        '''Display success message on console in green

        Arguments:

        msg -- text to be printed
        '''
        print(f"{Fore.GREEN}[+] {msg} {Style.RESET_ALL}")

    s1_color = '#6B0AEA' # Purple
    # Define template for bar of tqdm
    temp_bar_format = "\033[34m[i] Retrieved exit-nodes IP from Tor API {bar} {percentage:3.0f}% |{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"

    based_url = "https://check.torproject.org/exit-addresses"

    if not args.silent:
        if args.debug:
            infotext(f"s1_color : {s1_color}")
            infotext(f"temp_bar_format : {temp_bar_format}")
            infotext(f"based_url : {based_url}")
            if args.silent:
                infotext("The option -s or --silent is On")
            if args.export:
                infotext("The option -E or --export is On")

    ###########################################################################
    ######################## Now process for API CALL #########################
    ###########################################################################

    try:
        response_get = requests.get(based_url, timeout=300)
        if args.debug:
            infotext(f"Status code before test : {response_get.status_code}")
        response_get.raise_for_status() # Raises an exception for HTTP response codes 4xx and 5xx
        if response_get.status_code == 200:
            data_get = response_get.text
            if args.debug:
                infotext(f"All the data retrieved by the API GET call : {data_get}")
            if not args.silent:
                successtext(f"API requests has succeded (status code : {response_get.status_code}).")
    except requests.exceptions.RequestException as ex:
        if not args.silent:
            errortext(f"An error occurred while retrieving the data : \n{ex}.\n\n")
            errortext(f"And the status code of the API request is : {response_get.status_code}.")
        exit()

    pattern = r"ExitAddress (.+)"
    matches = re.findall(pattern, data_get)

    exit_nodes = []
    if not args.silent:
        exit_nodes_iter = tqdm(matches, unit=" IP", mininterval=0.1, maxinterval=5, smoothing=True, bar_format=temp_bar_format, colour=s1_color)
    else:
        exit_nodes_iter = matches

    for data_collected in exit_nodes_iter:
        data_collected = data_collected.split(" ")[0]
        exit_nodes.append(data_collected)

    if args.export:
        with open(args.export, 'w', encoding="utf-8") as file_opened:
            for item in exit_nodes:
                file_opened.write(f"{item}\n")
        if not args.silent:
            successtext(f"Exported the exit-nodes IP to '{args.export}'.")
        if args.debug:
            infotext(exit_nodes)
    else:
        if not args.silent:
            print(f"\n\n{exit_nodes}")
        else:
            print(exit_nodes)

if __name__ == "__main__":
    get_exit_nodes_ip(args.export, args.silent, args.debug)
