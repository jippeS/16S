#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

class MetaDatamaker:
    def __init__(self, args):
        self.forward_primer = args.forward_primer
        self.reverse_primer = args.reverse_primer
        self.input_list = args.input
        self.output_file = args.output


    # def opening_files(self):
    #     with open(self.input, "r") as f:
    #         file_list = f.read()
    #         print(file_list)
    def make_metadata(self):
        file = "#SampleID   Index code	Forward Primer	Reverse Primer	Description\n"
        index = 0
        for i in self.input_list:
            file_line = f"{i}   {index}  {self.forward_primer}  {self.reverse_primer}\n"
            index += 1
            file += file_line

        with open(self.output_file, "w") as f:
            f.write(file)




def argparser():
    """
    Reads the arguments from the command line.
    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--forward_primer", help="forward primer used.")
    parser.add_argument("--reverse_primer", help="reverse primer used")
    parser.add_argument("--input", help="metadata file. (samplename_client_id name")
    parser.add_argument("--output", help="metadata file. (samplename_client_id name")

    args = parser.parse_args()
    return args


def main():
    """
    Execute the Class function in order.
    """
    args = argparser()
    MetaData_maker = MetaDatamaker(args)
    MetaData_maker.opening_files()

if __name__ == '__main__':
    sys.exit(main())