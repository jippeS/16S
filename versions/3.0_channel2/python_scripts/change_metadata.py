#!/usr/bin/env python3
import configparser
import argparse
import sys


class Metadata(object):
    def __init__(self):
        args = argparser()
        self.inputfile = args.inputfile
        self.qn = args.qn

    def read_metadata(self):
        with open(self.inputfile, "r") as inputfile:
            header = inputfile.readline()
            contents = [i.split("\t") for i in inputfile.read().split("\n")][0:-1]
        return header, contents

    def get_new_contents(self, header, contents):
            new_contents = header
            for sample in contents:
                line = ""
                for item in sample:
                    if item is sample[0]:
                        line += f"{item}.{self.qn}\t"
                    else:
                        line += f"{item}\t"
                new_contents += f"{line.strip()}\n"
            print(new_contents)
            return new_contents

    def write_metadata(self, new_contents):
        with open(self.inputfile, "w+") as outputfile:
            outputfile.write(new_contents)


def argparser():
    """
    Reads the arguments from the command line.
    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="Must be a metadata file.")
    parser.add_argument("qn", help="Must be a Quote number.")

    args = parser.parse_args()
    return args


def main():
    """
    Execute the Class function in order.
    """
    pre_data = Metadata()
    header, contents = pre_data.read_metadata()
    new_contents = pre_data.get_new_contents(header, contents)
    pre_data.write_metadata(new_contents)

if __name__ == '__main__':
    sys.exit(main())
