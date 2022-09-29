# NamerVS (Namer State Validation Script)

NamerdBin will take a list of names and output the status of the names

## Installation


```bash
chmod +x setup.sh
./setup.sh
```

## Usage

usage: main.py [-h] -i INPUT -o OUTPUT [-v]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file containing list of names
  -o OUTPUT, --output OUTPUT
                        Output file to write results to
  -v, --verbose         Verbose output, will log to /var/log/namerdbin.log
