#!/usr/bin/python3

import json

my_string = """{
 "start": {
  "reserved": false,
  "week": 32,
  "start": 34272
 },
 "info": {
  "name": "buttsex",
  "nameHash": "72afdae5fe3d308d3fa03f135be476f43d1915809e22297f6ef2d7127d811718",
  "state": "CLOSED",
  "height": 54767,
  "renewal": 56967,
  "owner": {
   "hash": "b1491aed25c68c913ffe1d6d502009c436de52f5d8eb83471f13fe8d34d2785d",
   "index": 15
  },
  "value": 95000000,
  "highest": 4151000000,
  "data": "0002036e73310762757474736578002ce706b701c002",
  "transfer": 0,
  "revoked": 0,
  "claimed": 0,
  "renewals": 0,
  "registered": true,
  "expired": false,
  "weak": false,
  "stats": {
   "renewalPeriodStart": 56967,
   "renewalPeriodEnd": 162087,
   "blocksUntilExpire": 28497,
   "daysUntilExpire": 197.9
  }
 }
}"""

my_dict = json.loads(my_string)

new_dict = {
    "start": {
        "reserved": my_dict["start"]["reserved"],
        "week": my_dict["start"]["week"],
        "start": my_dict["start"]["start"]
    },
    "info": {
        "name": my_dict["info"]["name"],
    }
}

our_json = json.dumps(new_dict, indent=4)
print(f"{our_json}")

#puny to ascii function
def turn_puny_to_ascii(punycode):
    return punycode.encode('idna').decode('ascii')

#function to test if string is punycode returns true if punycode, false if not
def is_punycode(string):
    try:
        string.encode('idna')
    except UnicodeError:
        return False
    else:
        return True