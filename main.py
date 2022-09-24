#!/usr/bin/env python3
import subprocess
import sys
import argparse
import logging

import idna
import pandas as pd

LOGGER = logging.getLogger(__name__)


def arg_collection():
    """This function is to collect the arguments from the user"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input File name")
    parser.add_argument("-o", "--output", help="Output File name")
    args = parser.parse_args()
    return args


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


def main():
    """Main function"""

    our_arguments = arg_collection()
    # collect filename and output file from argparse
    filename = our_arguments.input
    outputfile = our_arguments.output

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

    translated = {}
    done = {}
    templst = []
    for x in data:
        try:
            translate = idna.decode(x)
            translate = translate.split(",")[0]
            state = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.state")
            reserved = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .start.reserved")
            if x[:4] != "xn--":
                if state == "OPENING":
                    templst.append("NA")
                    templst.append(state)
                    templst.append(reserved)
                    hoursuntilbidding = subprocess.getoutput(
                        f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilBidding")
                    templst.append(hoursuntilbidding)
                    templst.append("null")
                    templst.append("null")
                    templst.append("null")
                elif state == "BIDDING":
                    templst.append("NA")
                    templst.append(state)
                    templst.append(reserved)
                    hoursuntilreveal = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilReveal")
                    templst.append("null")
                    templst.append(hoursuntilreveal)
                    templst.append("null")
                    templst.append("null")
                elif state == "REVEAL":
                    templst.append("NA")
                    templst.append(state)
                    templst.append(reserved)
                    hoursuntilclose = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilClose")
                    templst.append("null")
                    templst.append("null")
                    templst.append(hoursuntilclose)
                    templst.append("null")
                elif state == "CLOSED":
                    templst.append("NA")
                    templst.append(state)
                    templst.append(reserved)
                    daysuntilexpire = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.daysUntilRedeem")
                    templst.append("null")
                    templst.append("null")
                    templst.append("null")
                    templst.append(daysuntilexpire)
                else:
                    templst.append("NA")
                    templst.append(state)
                    templst.append(reserved)
                    templst.append("null")
                    templst.append("null")
                    templst.append("null")
                    templst.append("null")
                translated[x] = templst
                templst = []
            else:

                if state == "OPENING":
                    templst.append(translate)
                    templst.append(state)
                    templst.append(reserved)
                    hoursuntilbidding = subprocess.getoutput(
                        f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilBidding")
                    templst.append(hoursuntilbidding)
                    templst.append("null")
                    templst.append("null")
                    templst.append("null")
                elif state == "BIDDING":
                    templst.append(translate)
                    templst.append(state)
                    templst.append(reserved)
                    hoursuntilreveal = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilReveal")
                    templst.append("null")
                    templst.append(hoursuntilreveal)
                    templst.append("null")
                    templst.append("null")
                elif state == "REVEAL":
                    templst.append(translate)
                    templst.append(state)
                    templst.append(reserved)
                    hoursuntilclose = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilClose")
                    templst.append("null")
                    templst.append("null")
                    templst.append(hoursuntilclose)
                    templst.append("null")
                    translated[x] = templst
                    templst = []
                elif state == "CLOSED":
                    templst.append(translate)
                    templst.append(state)
                    templst.append(reserved)
                    daysuntilexpire = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.daysUntilRedeem")
                    templst.append("null")
                    templst.append("null")
                    templst.append("null")
                    templst.append(daysuntilexpire)
                    translated[x] = templst
                    templst = []
                else:
                    templst.append(translate)
                    templst.append(state)
                    templst.append(reserved)
                    templst.append("null")
                    templst.append("null")
                    templst.append("null")
                    templst.append("null")
                    translated[x] = templst
                    templst = []
        except idna.InvalidCodepoint as e:
            elements = e.args
            translate = elements[0].split("\'")[1]
            state = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.state")
            reserved = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .start.reserved")
            if state == "OPENING":
                templst.append(translate)
                templst.append(state)
                templst.append(reserved)
                hoursuntilbidding = subprocess.getoutput(
                    f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilBidding")
                templst.append(hoursuntilbidding)
                templst.append("null")
                templst.append("null")
                templst.append("null")
                translated[x] = templst
                templst = []
            elif state == "BIDDING":
                templst.append(translate)
                templst.append(state)
                templst.append(reserved)
                hoursuntilreveal = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilReveal")
                templst.append("null")
                templst.append(hoursuntilreveal)
                templst.append("null")
                templst.append("null")
                translated[x] = templst
                templst = []
            elif state == "REVEAL":
                templst.append(translate)
                templst.append(state)
                templst.append(reserved)
                hoursuntilclose = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilClose")
                templst.append("null")
                templst.append("null")
                templst.append(hoursuntilclose)
                templst.append("null")
                translated[x] = templst
                templst = []
            elif state == "CLOSED":
                templst.append(translate)
                templst.append(state)
                templst.append(reserved)
                daysuntilexpire = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.daysUntilRedeem")
                templst.append("null")
                templst.append("null")
                templst.append("null")
                templst.append(daysuntilexpire)
                translated[x] = templst
                templst = []
            else:
                templst.append(translate)
                templst.append(state)
                templst.append(reserved)
                templst.append("null")
                templst.append("null")
                templst.append("null")
                templst.append("null")
                translated[x] = templst
                templst = []
        except Exception as e:
            state = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.state")
            reserved = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .start.reserved")
            if state == "OPENING":
                templst.append("Invalid")
                templst.append(state)
                templst.append(reserved)
                hoursuntilbidding = subprocess.getoutput(
                    f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilBidding")
                templst.append(hoursuntilbidding)
                templst.append("null")
                templst.append("null")
                templst.append("null")
                translated[x] = templst
                templst = []
            elif state == "BIDDING":
                templst.append("Invalid")
                templst.append(state)
                templst.append(reserved)
                hoursuntilreveal = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilReveal")
                templst.append("null")
                templst.append(hoursuntilreveal)
                templst.append("null")
                templst.append("null")
                translated[x] = templst
                templst = []
            elif state == "REVEAL":
                templst.append("Invalid")
                templst.append(state)
                templst.append(reserved)
                hoursuntilclose = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilClose")
                templst.append("null")
                templst.append("null")
                templst.append(hoursuntilclose)
                templst.append("null")
                translated[x] = templst
                templst = []
            elif state == "CLOSED":
                templst.append("Invalid")
                templst.append(state)
                templst.append(reserved)
                daysuntilexpire = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.daysUntilRedeem")
                templst.append("null")
                templst.append("null")
                templst.append("null")
                templst.append(daysuntilexpire)
                translated[x] = templst
                templst = []
            else:
                templst.append("Invalid")
                templst.append(state)
                templst.append(reserved)
                templst.append("null")
                templst.append("null")
                templst.append("null")
                templst.append("null")
                translated[x] = templst
                templst = []

    translated = {"name": translated.keys(), "decoded_punycode": [a[0] for a in translated.values()],
                  "status": [a[1] for a in translated.values()], "reserved": [a[2] for a in translated.values()],
                  "hoursuntilbidding": [a[3] for a in translated.values()],
                  "hoursuntilreveal": [a[4] for a in translated.values()],
                  "hoursuntilclose": [a[5] for a in translated.values()],
                  "daysuntilexpire": [a[6] for a in translated.values()]}
    nlst = []

    for key, value in translated.items():
        for i in value:
            nlst.append(i)
        done[key] = nlst
        nlst = []

    df = pd.DataFrame(done)
    df.to_csv(outputfile, index=None, encoding="utf-16", sep=",")
    LOGGER.info("Done!")


if __name__ == "__main__":
    """This is executed when run from the command line"""
    main()
