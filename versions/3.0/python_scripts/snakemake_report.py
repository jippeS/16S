#!/usr/bin/env python3

import configparser
import argparse
import sys
import os


class PreDemux:
    def __init__(self):
        args = argparser()
        self.inputdir = args.inputdir

    def Formatting_contents(self):
        file_text = ""
        with open(f"{self.inputdir}reports/Pipeline_execution.txt", 'r') as pipeline_file:
            report_list = [report.split("  ") for report in pipeline_file.read().split("@#") if "qiime" in report.strip()]
        for command in report_list:
            command_text = ""
            for line in command:
                line = line.strip()
                if not line.startswith("--"):
                    command_text += f"{line}\n"
                else:
                    command_text += f"\t{line}\n"
            file_text += f"{command_text}\n"
        report_output_file(file_text, f"{self.inputdir}reports/Qiime_report.txt")

    def Formatting_timestamps(self):
        folder_path = f"{self.inputdir}benchmarks/"  # Replace with the actual folder path

        file_names = []  # To store the file names

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_names.append(file_path)

        # Printing only the file names
        header = "name\ts\th:m:s\tmax_rss\tmax_vms\tmax_uss\tmax_pss\tio_in\tio_out\tmean_load\tcpu_time\n"
        time_dic = {}
        for file_path in file_names:
            file_name = os.path.basename(file_path)
            # print(file_path)
            # print(file_name)
            with open(file_path, "r") as bench_file:
                time_dic[file_name[:-4]] = bench_file.read().split("\n")[1].split("\t")
                values = time_dic[file_name[:-4]]
                header += f"{file_name[:-4]}\t{values[0]}\t{values[1]}\t{values[2]}\t{values[3]}\t{values[4]}\t{values[5]}\t{values[6]}\t{values[7]}\t{values[8]}\t{values[9]}\n"

        # print(len(time_dic["Classification"]))
        # print(time_dic)
        report_output_file(header, f"{self.inputdir}reports/time.csv")

        # total_time = 0
        # for item in time_dic.values():
        #     total_time += float(item[0])
        # threshold = round(total_time*(1/len(time_dic.items())))
        # print(total_time)
        # print(threshold)

def report_output_file(report, output_file):
        """
        Function for writing to files.
        :param output_file: name of the file
        :param report: The sentence or complete input that needs to be written to a file.
        :param name: The name were the report should be written to.
        """
        if os.path.isfile(output_file):
            with open(output_file, 'a') as file:
                file.write(report)
                file.close()
        else:
            with open(output_file, "w+") as file:
                file.write(report)
                file.close()
def argparser():
    """
    Reads the arguments from the command line.
    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir", help="input file must be a fasta file.")

    args = parser.parse_args()
    return args


def main():
    """
    Execute the Class function in order.
    """
    pre_demux_calculation = PreDemux()
    pre_demux_calculation.Formatting_contents()
    pre_demux_calculation.Formatting_timestamps()

if __name__ == '__main__':
    sys.exit(main())