#!/usr/bin/env python3
"""
Runs FLOSS to extract (even some obfuscated) strings from a binary and correlates them to a list of suspicious API
calls/combinations

Usage: floss-suspicious.py -f FILENAME

Options:
    -f FILENAME --filename=FILENAME  Use this binary file as input
"""
import os
import subprocess
import sys

from docopt import docopt
from schema import Schema, SchemaError


def main():
    """Read binary file and correlate API calls."""
    args = docopt(__doc__)
    schema = Schema({'--filename': os.path.exists})
    try:
        args = schema.validate(args)
    except SchemaError as error:
        exit(error)
    floss = subprocess.run(["floss", args['--filename']], capture_output=True)
    with open("floss-suspicious.txt", 'r') as suspicious:
        suspicious_api_lines = [suspicious_api_line.strip() for suspicious_api_line in suspicious.readlines()]
    with open(f'{args["--filename"]}_floss.txt', 'w') as floss_output:
        floss_output.writelines(floss.stdout.decode())
        print(f'Floss output written to {args["--filename"]}_floss.txt')
    for suspicious_apis in suspicious_api_lines:
        for suspicious_api in suspicious_apis.split(' AND '):
            if suspicious_api not in floss.stdout.decode().split('\n'):
                break
        else:
            print(f'Found suspicious API combination: {suspicious_apis}')
            with open(f'{args["--filename"]}_floss.txt', 'a') as floss_output:
                floss_output.write(f'Found suspicious API combination: {suspicious_apis}\n')


if __name__ == "__main__":
    main()
