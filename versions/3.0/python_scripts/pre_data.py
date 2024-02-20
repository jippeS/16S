#!/usr/bin/env python3
import configparser
import argparse
import sys
import zipfile
import os
import gzip
import shutil

class PreData:
    def __init__(self):
        args = argparser()
        self.inputdir = args.inputdir

    def opening_files(self):
        # Path to your zip file
        folder_path = self.inputdir

        # Directory where you want to extract the files
        extracted_folder = f'{folder_path}input'

        # Create the target directory if it doesn't exist
        if not os.path.exists(extracted_folder):
            os.makedirs(extracted_folder)

        files_in_folder = os.listdir(folder_path)
        print(files_in_folder)
        # Check if there is at least one file in the folder
        if not files_in_folder:
            print("No files found in the specified folder.")
        else:
            # Assume the first file in the folder is the zip file
            zip_file_name = ""
            for zip_file in files_in_folder:
                if zip_file != "output" and zip_file != "input":
                    zip_file_name = zip_file

            zip_file_path = os.path.join(folder_path, zip_file_name)
            # Open the zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Extract all contents to the target directory
                zip_ref.extractall(extracted_folder)

            # Now, you can iterate through the folders and retrieve all files
            for root, dirs, files in os.walk(extracted_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Do whatever you want with the file, for example, move it to another directory
                    # In this example, moving the file to 'pre_data_process' folder
                    destination_path = os.path.join(extracted_folder, file)
                    os.rename(file_path, destination_path)

            print("Files extracted and moved to 'pre_data_process' folder.")
        return extracted_folder

    def unzipping_gz(self, extracted_folder):
        files_in_folder = os.listdir(extracted_folder)
        # Path for the decompressed file (remove .gz extension)
        for file in files_in_folder:
            if file.endswith(".gz"):
                compressed_file = f"{extracted_folder}/{file}"

                if "_R1_" in file:
                    decompressed_file = f"{extracted_folder}/forward1.fastq"
                elif "_R2_" in file:
                    decompressed_file = f"{extracted_folder}/reverse1.fastq"
                else:
                    sys.exit(print("Something went terribly wrong call a medic!"))

                with gzip.open(compressed_file, 'rb') as compressed:
                    with open(decompressed_file, 'wb') as decompressed:
                        shutil.copyfileobj(compressed, decompressed)

        return 0

    def cleanup_gz(self, extracted_folder):

        # List all files in the directory
        files = os.listdir(extracted_folder)

        # Filter files ending with '.gz'
        gz_files = [file for file in files if file.endswith('.gz')]

        # Remove each '.gz' file
        for gz_file in gz_files:
            file_path = os.path.join(extracted_folder, gz_file)
            os.remove(file_path)
            print(f"Removed: {gz_file}")
        return 0


def argparser():
    """
    Reads the arguments from the command line.
    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("inputdir", help="Must be an input directory containing 1 file.")

    args = parser.parse_args()
    return args


def main():
    """
    Execute the Class function in order.
    """
    pre_data = PreData()
    extracted_folder = pre_data.opening_files()
    pre_data.unzipping_gz(extracted_folder)
    pre_data.cleanup_gz(extracted_folder)

if __name__ == '__main__':
    sys.exit(main())