#!/usr/bin/env python3
"""
Runs FLOSS to extract (even some obfuscated) strings from a binary and correlates them to a list of suspicious API
calls/combinations

Usage: floss-suspicious.py -f FILENAME [-s SUSPICIOUS]

Options:
    -f FILENAME --filename=FILENAME        Use this binary file as input
    -s SUSPICIOUS --suspicious=SUSPICIOUS  Use this configuration file [default: floss-suspicious.txt]
"""
import os
import subprocess
import sys

from docopt import docopt
from schema import Schema, SchemaError, Optional


def read_config(path: str) -> dict:
    """
    Read a config file and return its contents as a dictionary for easier use.

    Parameters
    ----------
    path : str
        Path to the config file

    Returns
    -------
    dict
        Dictionary in the following form: {"description": [["one", "of", "these"], ["and", "one", "of", "these"]]}
    """
    with open(path, 'r') as configuration_file:
        configuration = {}
        for line in configuration_file.readlines():
            description = line.split(':')[1].strip()
            ands = line.split(':')[0].split(' AND ')
            for idx, combination in enumerate(ands):
                ors = combination.split(' OR ')
                ands[idx] = ors
            configuration[description] = ands
    return configuration


def find_suspicious_combinations(floss_output: str, suspicious_apis: dict) -> dict:
    """
    Find all suspicious API combinations and return them as a dict.

    Params
    ------
    floss_output : str
        Output generated by FLOSS string extraction
    suspicious_apis : dict
        Dictionary of suspicious API call combinations in the form of
        {"description": [["this", "or", "this"], ["and", "either", "of", "these"]]}

    Returns
    -------
    dict
        A dictionary with all suspicious combinations
    """
    suspicious_combinations_found = {}
    # Cache single suspicious API for easier comparison if a complete check is needed
    single_suspicious_apis = set()
    for suspicious_api_combinations in suspicious_apis.values():
        for suspicious_api_ors in suspicious_api_combinations:
            for suspicious_api in suspicious_api_ors:
                single_suspicious_apis.add(suspicious_api)
    # Try to find all calls to suspicious APIs in the FLOSS output
    suspicious_apis_found = set()
    for line in floss_output.split('\n'):
        if line in single_suspicious_apis:
            suspicious_apis_found.add(line)
    # Now let's check if enough APIs are found to form the suspicious combinations
    for description, suspicious_api_combinations in suspicious_apis.items():
        suspicious_combination = []
        for ors in suspicious_api_combinations:
            for api in ors:
                if api in suspicious_apis_found:
                    suspicious_combination.append(api)
                    break
            else:
                # Found at least one of the OR clauses
                break
        else:
            # Found all of the AND clauses, note exact combination
            suspicious_combinations_found[description] = suspicious_combination
    return suspicious_combinations_found


def main():
    """Read binary file and correlate API calls."""
    # Parse command line arguments
    args = docopt(__doc__)
    schema = Schema({'--filename': os.path.exists,
        Optional('--suspicious'): os.path.exists})
    try:
        args = schema.validate(args)
    except SchemaError as error:
        exit(error)
    # Read configuration file
    suspicious_apis = read_config(args['--suspicious'])
    # Run FLOSS
    floss = subprocess.run(["floss", args['--filename']], capture_output=True)
    with open(f'{args["--filename"]}_floss.txt', 'w') as floss_output:
        floss_output.writelines(floss.stdout.decode())
        print(f'Floss output written to {args["--filename"]}_floss.txt')
    # Find suspicious API combinations
    suspicious_combinations = find_suspicious_combinations(floss.stdout.decode(), suspicious_apis)
    if suspicious_combinations:
        print('Found suspicious API combinations: ')
        for description, suspicious_combination in suspicious_combinations.items():
            print(f'- {description}: {", ".join(suspicious_combination)}')
        with open(f'{args["--filename"]}_floss.txt', 'a') as floss_output:
            floss_output.write(f'Found suspicious API combinations:\n')
            for description, suspicious_combination in suspicious_combinations.items():
                floss_output.write(f'- {description}: {", ".join(suspicious_combination)}\n')


if __name__ == "__main__":
    main()
