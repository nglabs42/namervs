#!/usr/bin/env python3
import subprocess
import sys
import argparse
import logging

import idna
import pandas as pd

LOGGER = logging.getLogger(__name__)


def arg_collection(args):
    """This function is to collect the arguments
        from the user, includes help if help is triggered
        return help then exit"""

    parser = argparse.ArgumentParser(
        description="This script will take a list of names and output the status of the names"
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Input file containing list of names",
        required=True,
        type=str,
    )
    parser.add_argument(
        #  update to be required if -c/--csv is used
        "-o",
        "--output",
        help="Output file to write results to",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose output, will log to /var/log/namerdbin.log",
        required=False,
        action="store_true",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="/var/log/namerdbin.log",
    )


def is_punycode(our_string):
    """Tests if string is punycode"""

    try:
        idna.decode(our_string)

    except idna.InvalidCodepoint:
        return True
    except UnicodeError:
        return False
    else:
        return True


def decoded_punycode(our_string):
    """Decodes punycode and returns decoded punycode if possible"""

    try:
        translate = idna.decode(our_string)
        translate = translate.split(",")[0]
    except idna.InvalidCodepoint as e:
        elements = e.args
        translate = elements[0].split("\'")[1]
    return translate


def default_name_data(x):
    """Run hsd-cli to capture state and reserved status of name"""
    # in the future this will run once to capture each names data and parse from there
    # using hsd-cli rpc getnameinfo {x} --json
    state = subprocess.getoutput(
        f"hsd-cli rpc getnameinfo {x}|jq .info.state"
    )
    reserved = subprocess.getoutput(
        f"hsd-cli rpc getnameinfo {x}|jq .start.reserved"
    )
    return state, reserved


# This function will capture data points for "OPENING" auctions
def open_state(x, translate, state, reserved):
    """Capturing and Writing Data for "OPENING" State for {x}"""
    templst = list()
    templst.append(translate)
    templst.append(state)
    templst.append(reserved)
    hoursuntilbidding = subprocess.getoutput(
        f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilBidding"
    )
    templst.append(hoursuntilbidding)
    templst.append("")
    templst.append("")
    templst.append("")
    return templst


def bidding_state(x, translate, state, reserved):
    """Capturing and Writing Data for "BIDDING" State for {x}"""
    templst = list()
    templst.append(translate)
    templst.append(state)
    templst.append(reserved)
    hoursuntilreveal = subprocess.getoutput(
        f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilReveal"
    )
    templst.append("")
    templst.append(hoursuntilreveal)
    templst.append("")
    templst.append("")
    return templst


def reveal_state(x, translate, state, reserved):
    """Capturing and Writing Data for "REVEAL" State for {x}"""
    templst = list()
    templst.append(translate)
    templst.append(state)
    templst.append(reserved)
    hoursuntilclose = subprocess.getoutput(
        f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilClose"
    )
    templst.append("")
    templst.append("")
    templst.append(hoursuntilclose)
    templst.append("")
    return templst


def closed_state(x, translate, state, reserved):
    """Capturing and Writing Data for "CLOSED" State for {x}"""
    templst = list()
    templst.append(translate)
    templst.append(state)
    templst.append(reserved)
    daysuntilexpire = subprocess.getoutput(
        f"hsd-cli rpc getnameinfo {x}|jq .info.stats.daysUntilExpire"
    )
    templst.append("")
    templst.append("")
    templst.append("")
    templst.append(daysuntilexpire)
    return templst


def no_state(translate, state, reserved):
    """Capturing and Writing Data for "NO STATE" State for {x}"""
    templst = list()
    templst.append(translate)
    templst.append(state)
    templst.append(reserved)
    templst.append("")
    templst.append("")
    templst.append("")
    templst.append("")
    return templst


def main(args):
    """Main function"""

    our_arguments = arg_collection(args)
    # collect filename and output file from argparse
    filename = our_arguments.input
    outputfile = our_arguments.output
    verbose = our_arguments.verbose

    if verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)

    try:
        with open(filename) as f:
            data = f.readlines()[1:]
    except Exception as error:
        LOGGER.error("Input File not found %s", error)
        sys.exit(1)

    data = [x.strip() for x in data]

    # if data is empty log error and exit
    if not data:
        LOGGER.error("Input File is empty")
        sys.exit(1)

    if data == "":
        LOGGER.error("Input File is empty")
        sys.exit(1)

    translated = {}
    done = {}
    for x in data:
        if is_punycode(x):
            # if x is punycode decode it and store as translate or pass x to translate
            translate = decoded_punycode(x)
        else:
            translate = x
        # Capture default data for all names State and Reserved
        state, reserved = default_name_data(x)
        # for "OPENING" state
        if state == '"OPENING"':
            # call "OPENING" function
            templst = open_state(x, translate, state, reserved)
            translated[x] = templst
        # for "BIDDING" state
        elif state == '"BIDDING"':
            # call "BIDDING" function
            templst = bidding_state(x, translate, state, reserved)
            translated[x] = templst
        # for "REVEAL" state
        elif state == '"REVEAL"':
            templst = reveal_state(x, translate, state, reserved)
            translated[x] = templst
        # for "CLOSED" state
        elif state == '"CLOSED"':
            # call "CLOSED" function
            templst = closed_state(x, translate, state, reserved)
            translated[x] = templst
        # for all other stateor no data
        else:
            # for "NO STATE" or unknown states
            templst = no_state(translate, state, reserved)
            translated[x] = templst
    translated = {
        "name": translated.keys(),
        "decoded_punycode": [a[0] for a in translated.values()],
        "status": [a[1] for a in translated.values()],
        "reserved": [a[2] for a in translated.values()],
        "hoursuntilbidding": [a[3] for a in translated.values()],
        "hoursuntilreveal": [a[4] for a in translated.values()],
        "hoursuntilclose": [a[5] for a in translated.values()],
        "daysuntilexpire": [a[6] for a in translated.values()]
    }
    nlst = []

    for key, value in translated.items():
        for i in value:
            nlst.append(i)
        done[key] = nlst
        nlst = []

        df = pd.DataFrame(done)
        # if -c/--cvs is set write to csv outputfile
        #  if our_arguments.csv:
        df.to_csv(outputfile, index=None, encoding="utf-16", sep=",")

        LOGGER.info("Done!")


if __name__ == "__main__":
    """This is executed when run from the command line passing command line arguments to main function"""

    main(sys.argv[1:])
