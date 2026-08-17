import os
from Bio import SeqIO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
import codecs
import configparser

config = configparser.ConfigParser()
config.read('/export2/home/microlab/microlab/python_scripts/qiime/qiime_settings.ini')

#inputfile = "10kseq_files.txt"

os.system("[0-9]*.fastq;ls [0-9]*.fastq > subset_files.txt") #*.fastq.gz ls [A-Z]*.fastq > list_fastq_10kseq.txt") "cd " + path + ";gzip -f -k [0-9]*.fastq;chmod -R 777 [0-9]*.fastq.gz;ls [0-9]*.fastq.gz > 10kseq_files.txt")

inputfiles_subset = open("subset_files.txt", "r") #rU
file_list_subset = set()

output_quality = open("quality_scores_datasets.txt", "w+") 

def transpose(phred_score, phred_score_transpose):

    max_length = 0   
    for j in phred_score:
        length = len(j)
        if length >= max_length:
            max_length = length
        else:
            continue

    for i in range(max_length): #for i in range(len(l1[0])):
        #print(i)
        row =[] 
        for item in phred_score:
            try:
                row.append(item[i])
                #print(row)
            except:
                continue
        phred_score_transpose.append(row) 
    return phred_score_transpose 



def distribution_read_lengths (number_reads, sizes):
    size_distribution = []
    size_counter = Counter(sizes).items()
    size_distribution0 = [ [a,b] for a,b in size_counter ] # verdeling read-lengths, zorgen dat >1% wordt geprint
    for item in size_distribution0:
        if item[1] >= (0.01 * int(number_reads)):
            size_distribution.append(item)
        else:
            continue
    
    return (size_distribution)

#phred_score = [[1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5,6], [1,2,3,4]]


for inputfile_subset in inputfiles_subset:
    inputfile_subset0 = inputfile_subset.strip('\n')
    
    item1 = inputfile_subset0.split("@")
    identifier = item1[0] #RBAR_01_20200115
    file_list_subset.add(identifier)
    if "_R1_" in inputfile_subset0:
        seq_set = "forward"
    else:
        seq_set = "reverse"
        
    sizes = list()
    phred_score = list()
    phred_score_transpose = list()
    #print(inputfile_10kseq0, identifier, seq_set)
    
    with open(inputfile_subset0, "r") as handle: #rU
        #print ("tot punt1 doet ie het!" )
        for record in SeqIO.parse(handle, "fastq"):
            #print ("tot punt2 doet ie het!" )
            #print (record)#rU
            size_seq = len(record.seq)
            sizes.append(size_seq)
            quality_seq = record.letter_annotations["phred_quality"]
            #print (quality_seq)
            #quality_seq = [int(x) for x in quality_seq0]
            #print (quality_seq)
            phred_score.append(quality_seq)
            
            size_counter = Counter(sizes).items()
            size_distribution = [ [a,b] for a,b in size_counter ] # verdeling read-lengths, zorgen dat >1% wordt geprint
        

        phred_score_transpose = transpose(phred_score,phred_score_transpose)
        #print (phred_score_transpose)
        
        phred_score_transpose_df = pd.DataFrame(phred_score_transpose)
        #phred_score_transpose_df.to_csv(identifier + seq_set + "_phred_score_transpose.csv",sep='\t', index=False)

        pos = 1
        length_reads = len(phred_score_transpose)
        number_reads = len(phred_score)

        size_distribution = distribution_read_lengths (number_reads, sizes)    
        

        q90_list = list()
        q75_list = list()
        q50_list = list()
        q25_list = list()
        q10_list = list()

        q50_e30_list = list()
        q50_e27_list = list()
        q50_e25_list = list()
        q50_e22_list = list()
        q50_e20_list = list()

        

        for item in phred_score_transpose [0:]:
            #print (line)
            line_array = np.array(item)
            #print(line_array)

            q90 = np.percentile(line_array, 90)
            q75 = np.percentile(line_array, 75)
            q50 = np.percentile(line_array, 50)
            q25 = np.percentile(line_array, 25)
            q10 = np.percentile(line_array, 10)
            
            #print("pos: ", pos, q90,q75,q50,q25,q10)
                
            #q90 = line_array.quantile([0.9])
                
            if (q90 <= 30) and len(q90_list) == 0:
                q90_list.append(pos)

            if (q75 <= 30) and len(q75_list) == 0:
                q75_list.append(pos)
            
            if (q50 <= 30) and len(q50_list) == 0:
                q50_list.append(pos)
            
            if (q25 <= 30) and len(q25_list) == 0:
                q25_list.append(pos)

            if (q10 <= 30) and len(q10_list) == 0:
                q10_list.append(pos)


            if (q50 <= 30) and len(q50_e30_list) == 0:
                q50_e30_list.append(pos)

            if (q50 <= 27.5) and len(q50_e27_list) == 0:
                q50_e27_list.append(pos)

            if (q50 <= 25) and len(q50_e25_list) == 0:
                q50_e25_list.append(pos)

            if (q50 <= 22.5) and len(q50_e22_list) == 0:
                q50_e22_list.append(pos)

            if (q50 <= 20) and len(q50_e20_list) == 0:
                q50_e20_list.append(pos)

                
            
            #else:
                #continue

            pos += 1
                #percentile = quality_seq_pd.quantile([0.9, 0.75, 0.5, 0.25, 0.1])
        #print (q90_list, q75_list, q50_list, q25_list, q10_list)
        #print(length_reads)

        line_quality = ("############################################################################################################################" + "\n\n"
                        + "data set: " + identifier + " " + seq_set + "\n"
                        + "length_reads: " + str(length_reads) + "\n"
                        + "percentile_90 < 30 at position: " + str(q90_list) + "\n"
                        + "percentile_75 < 30 at position: " + str(q75_list) + "\n"
                        + "percentile_50 < 30 at position: " + str(q50_list) + "\n"
                        + "percentile_25 < 30 at position: " + str(q25_list) + "\n"
                        + "percentile_10 < 30 at position: " + str(q10_list) + "\n"
                        + "number_reads: " + str(number_reads) + "\n"
                        + "perc_50: " + "quality <30.0 pos: " + str(q50_e30_list) + "\n"
                        + "         " + "quality <27.5 pos: " + str(q50_e27_list) + "\n"
                        + "         " + "quality <25.0 pos: " + str(q50_e25_list) + "\n"
                        + "         " + "quality <22.5 pos: " + str(q50_e22_list) + "\n"
                        + "         " + "quality <20.0 pos: " + str(q50_e20_list) + "\n"
                        + "length_distribution (>= 1 % of the reads): " + "\n"
                        + str(size_distribution) + "\n\n\n")
        
        print(line_quality)
        #print(size_distribution)
        output_quality.write(line_quality)

output_quality.close()

#os.system("cd " + path + ";gzip -f -k [0-9]*.fastq")    
