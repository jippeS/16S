import Bio
from Bio import SeqUtils
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from Bio import SeqIO
import glob2
import configparser

config = configparser.ConfigParser()
config.read('/export2/home/microlab/microlab/python_scripts/qiime/qiime_settings.ini')

#inputfile = "10kseq_files.txt"

#path = config['qiime']['path']


forward_primer = config['qiime']['forward_primer']  #forward_primer = "GTGYCAGCMGCCGCGGTAA"
reverse_primer = config['qiime']['reverse_primer']  #reverse_primer = "CCGYCAATTYMTTTRAGTTT"


#allFiles = glob.glob("2kseq_RBAR_05_20200409@SAM1-5_S3_L001_R*_001.fastq")

fastq_R1_file = glob2.glob("*@*_R1_*.fastq") #("2kseq_RBAR_05_20200409@SAM1-5_S3_L001_R1_001.fastq") ("100_R1_.fastq")
fastq_R2_file = glob2.glob("*@*_R2_*.fastq") #("2kseq_RBAR_05_20200409@SAM1-5_S3_L001_R2_001.fastq") ("100_R2_.fastq")
fastq_R1_file_str = str(fastq_R1_file) [2:-2]
fastq_R2_file_str = str(fastq_R2_file) [2:-2]

output_forward = open("./raw_data/forward.fastq", "w+")
output_reverse = open("./raw_data/reverse.fastq", "w+")

#forward_primer = "GTGYCAGCMGCCGCGGTAA"
#reverse_primer = "CCGYCAATTYMTTTRAGTTT"

primers_allseq_fwd = list()
forward_primer0 = Seq(forward_primer)
#primers_allseq_fwd.append(forward_primer0)

primers_allseq_rev = list()
reverse_primer0 = Seq(reverse_primer)
#reverse_primer0 = reverse_primer1.reverse_complement()
#primers_allseq_rev.append(reverse_primer0)
#primer_compl = primer0.reverse_complement()

with open (fastq_R1_file_str, "r") as handle_fwd: 
    with open (fastq_R2_file_str, "r") as handle_rev: 
        count = 3

        for line_fwd, line_rev in zip(handle_fwd, handle_rev):
            count += 1

            if count % 4 == 0:                
                header_fwd = str(line_fwd) #[:-1]
                header_rev = str(line_rev)
                    
            elif count % 4 == 1:
                seq_fwd = str(Seq(line_fwd))
                seq_rev = str(Seq(line_rev))
                
            elif count % 4 == 2:
                line_3_fwd = str(line_fwd)
                line_3_rev = str(line_rev)

            elif count % 4 == 3:
                qual_fwd = str(line_fwd)
                qual_rev = str(line_rev)
                               
                fwd_match_line_fwd = SeqUtils.nt_search(seq_fwd, forward_primer0)
                fwd_match_line_rev = SeqUtils.nt_search(seq_rev, forward_primer0)
                
                rev_match_line_fwd = SeqUtils.nt_search(seq_fwd, reverse_primer0)
                rev_match_line_rev = SeqUtils.nt_search(seq_rev, reverse_primer0)

                if len(fwd_match_line_fwd) > 1  or len(rev_match_line_rev) > 1:
                    
                    fastq_fwd = (header_fwd + seq_fwd + line_3_fwd + qual_fwd)
                    fastq_rev = (header_rev + seq_rev + line_3_rev + qual_rev)
                    output_forward.write(fastq_fwd)
                    output_reverse.write(fastq_rev)

                    header_fwd = ""
                    header_rev = ""
                    seq_fwd = ""
                    seq_rev = ""
                    line_3_fwd = ""
                    line_3_rev = ""
                    qual_fwd = ""
                    qual_rev = ""

                    fwd_match_line_fwd = ""
                    fwd_match_line_rev = ""
                    rev_match_line_fwd = ""
                    rev_match_line_rev = ""
                    continue
                   
                elif len(rev_match_line_fwd) > 1  or len(fwd_match_line_rev) > 1:

                    fastq_fwd = (header_fwd + seq_fwd + line_3_fwd + qual_fwd)
                    fastq_rev = (header_rev + seq_rev + line_3_rev + qual_rev)
                    output_forward.write(fastq_rev)
                    output_reverse.write(fastq_fwd)

                    header_fwd = ""
                    header_rev = ""
                    seq_fwd = ""
                    seq_rev = ""
                    line_3_fwd = ""
                    line_3_rev = ""
                    qual_fwd = ""
                    qual_rev = ""

                    fwd_match_line_fwd = ""
                    fwd_match_line_rev = ""
                    rev_match_line_fwd = ""
                    rev_match_line_rev = ""
                    continue
     
                else:
                    header_fwd = ""
                    header_rev = ""
                    seq_fwd = ""
                    seq_rev = ""
                    line_3_fwd = ""
                    line_3_rev = ""
                    qual_fwd = ""
                    qual_rev = ""

                    fwd_match_line_fwd = ""
                    fwd_match_line_rev = ""
                    rev_match_line_fwd = ""
                    rev_match_line_rev = ""

                    continue
              
            else:
                continue


output_forward.close()
output_reverse.close()
 
