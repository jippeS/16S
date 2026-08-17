#!/usr/bin/env python3
import configparser
import argparse
import sys
import zipfile
import os
import gzip
import shutil

class Restructure:
    def __init__(self):
        args = argparser()
        self.files = args.i
        self.bash_script = args.input_file
        self.inputdir = args.inputdir
        self.rest_name = args.name

    def open_file(self):
        with open(self.bash_script, "r+") as file:
            # Read the file's current contents
            contents = file.read()

            contents = contents.split("\n")
            new_contents = ""
            for line in contents:
                if line.startswith("qiime"):
                    change_line = line.strip()
                    new_contents += self.change_line(change_line)
                else:
                    new_contents += f"{line.strip()}\n"

            # Move the cursor to the beginning of the file
            file.seek(0)
            # Write the modified contents back
            file.write(new_contents)
            # Truncate the file to the new length (in case the new content is shorter)
            file.truncate()

    def change_line(self, change_line):
        changed_line = ""
        change_line = change_line.split("--i")
        changed_line += f"{change_line[0]}--i"
        change_line = change_line[1].split(" ")
        changed_line += change_line[0]
        for name in self.files:
            changed_line += f" {self.inputdir}{name}{self.rest_name}"

        return changed_line
def argparser():
    """
    Reads the arguments from the command line.
    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('i', nargs='+', type=str, help="dataset names")
    parser.add_argument("--input_file", help="inputbash")
    parser.add_argument("--inputdir", help="inputdir")
    parser.add_argument("--name", help="name")

    args = parser.parse_args()
    return args


def main():
    """
    Execute the Class function in order.
    """
    pre_data = Restructure()
    pre_data.open_file()

if __name__ == '__main__':
    sys.exit(main())