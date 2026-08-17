#!/usr/bin/env python3
import Bio
from Bio import SeqUtils
from Bio.Seq import Seq
from Bio import SeqIO
import configparser
import argparse
import sys
import yaml

def sorting_sequences(handle_fwd, handle_rev, output_forward, output_reverse, forward_primer, reverse_primer):
    count = 3
    for line_fwd, line_rev in zip(handle_fwd, handle_rev):
        count += 1
        # Retrieve the header.
        if count % 4 == 0:
            header_fwd = str(line_fwd)
            header_rev = str(line_rev)
        # Retrieve the sequence.
        elif count % 4 == 1:
            seq_fwd = str(Seq(line_fwd))
            seq_rev = str(Seq(line_rev))
        # Retrieve the + sign.
        elif count % 4 == 2:
            line_3_fwd = str(line_fwd)
            line_3_rev = str(line_rev)
        # Retrieve the quality sequence.
        elif count % 4 == 3:
            qual_fwd = str(line_fwd)
            qual_rev = str(line_rev)

            # Search the forward and reverse sequences for forward or reverse primers and put them in
            # their respective files.
            fwd_match_line_fwd = SeqUtils.nt_search(seq_fwd, forward_primer)
            fwd_match_line_rev = SeqUtils.nt_search(seq_rev, forward_primer)

            rev_match_line_fwd = SeqUtils.nt_search(seq_fwd, reverse_primer)
            rev_match_line_rev = SeqUtils.nt_search(seq_rev, reverse_primer)

            if len(fwd_match_line_fwd) > 1 or len(rev_match_line_rev) > 1:

                fastq_fwd = header_fwd + seq_fwd + line_3_fwd + qual_fwd
                fastq_rev = header_rev + seq_rev + line_3_rev + qual_rev
                output_forward.write(fastq_fwd)
                output_reverse.write(fastq_rev)

            elif len(rev_match_line_fwd) > 1 or len(fwd_match_line_rev) > 1:

                fastq_fwd = header_fwd + seq_fwd + line_3_fwd + qual_fwd
                fastq_rev = header_rev + seq_rev + line_3_rev + qual_rev
                output_forward.write(fastq_rev)
                output_reverse.write(fastq_fwd)


class PreDemux:
    def __init__(self):
        args = argparser()
        self.inputdir = args.inputdir

    def opening_files(self):
        # # Read the config file.
        # config = configparser.ConfigParser()
        # # config.read(f"/export/jippe/jsil/programs/16S/versions/3.0/config.yaml")
        # config.read(f"{self.inputdir}output/config.yaml")
        with open(f"{self.inputdir}output/config.yaml", 'r') as f:
            config = yaml.safe_load(f)

        # Put the primers in a seq object.
        forward_primer0 = config['forward']  # forward_primer = "GTGYCAGCMGCCGCGGTAA"
        reverse_primer0 = config['reverse']  # reverse_primer = "CCGYCAATTYMTTTRAGTTT"
        forward_primer = Seq(forward_primer0)
        reverse_primer = Seq(reverse_primer0)
        # Retrieve locations for the forward and reverse files.
        fastq_R1_file = f"{self.inputdir}input/raw_data/forward1.fastq"
        fastq_R2_file = f"{self.inputdir}input/raw_data/reverse1.fastq"

        # Retrieve locations for the future forward and reverse files.
        output_forward_file = f"{self.inputdir}input/raw_data/forward.fastq"
        output_reverse_file = f"{self.inputdir}input/raw_data/reverse.fastq"

        # Opens the files containing the sequences.
        with open(fastq_R1_file, "r") as handle_fwd:
            with open(fastq_R2_file, "r") as handle_rev:
                # Opens the files where the data is getting written to.
                with open(output_forward_file, "w+") as output_forward:
                    with open(output_reverse_file, "w+") as output_reverse:
                        # Calculating forward and reverse sequences.
                        sorting_sequences(handle_fwd, handle_rev, output_forward, output_reverse, forward_primer,
                                          reverse_primer)


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
    pre_demux_calculation.opening_files()

if __name__ == '__main__':
    sys.exit(main())