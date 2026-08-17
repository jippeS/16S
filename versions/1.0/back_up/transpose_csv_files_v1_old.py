import pandas as pd
import csv
import glob2
from Bio import SeqIO
from Bio.Seq import Seq
import numpy as np





#inputFile = 'level-3.csv'


def create_transposed_file (inputFile, initial):

    outputFile = initial + "_transpose_" + inputFile

    output = open(outputFile, 'w+')

    
    data = pd.read_csv(inputFile, sep=",") #pd.read_csv(input_unknowns_file, sep="\t", names=col_Names)

    transposed_data = data.transpose() #transposed_data = data.set_index('Description').transpose()

    transposed_data.to_csv(output, sep='\t', decimal='.', line_terminator = '\r', index=True)

    return

def tax_summaries_percentages (inputFile, initial):

    inputFile2 = initial + "_transpose_" + inputFile
    data1 = open(inputFile2, 'r')
    
    outputFile2 = initial + "_absolute_data_" + inputFile
    output2 = open(outputFile2, 'w+')

    for line in data1: #D_0__Bacteria;D_1__Synerg     Description	JPER_001	JPER_002	JPER_003
        #print(line)
        if "Description\t" in line:
            output2.write(line)
            data1.close()
            break
        else:
            continue

    data1 = open(inputFile2, 'r')
    for line in data1:
        if "D_0__" in line:
            output2.write(line)
        else:
            continue

    output2.close()
    data1.close()

    outputFile3 = initial + "_relative_data_" + inputFile
    output3 = open(outputFile3, 'w+')
    

    data = pd.read_csv(initial + "_absolute_data_" + inputFile, sep="\t") #pd.read_csv(input_unknowns_file, sep="\t", names=col_Names)
    print(data)

    data_num = data.select_dtypes(include=[np.number])

    print(data_num)

    data_num_pct = data_num/data_num[data_num.columns].sum()*100
    print(data_num_pct)
    data[data_num_pct.columns] = data_num_pct
    data_pct = data
    print(data_pct)

    data_pct.to_csv(output3, sep='\t', decimal='.', line_terminator = '\r', index=True) 

    output3.close()

    
    return



initial_list = glob2.glob("*.id")
initial0 = initial_list[0]     
initial = str(initial0[:-3])    
print(initial)



#os.system("ls level-*.csv > list_csv_files.txt") #####     OP CLUSTER AANZETTEN!


csv_files = open("list_csv_files.txt", "r")

for csv_file in csv_files:

    inputFile = csv_file.strip('\n')
    
    
    #item1 = inputfile_subset0.split("@")
    #identifier = item1[0] #RBAR_01_20200115
    #file_list_subset.add(identifier)
    #if "_R1_" in inputfile_subset0:
    #    seq_set = "forward"
    #else:
     #   seq_set = "reverse"
        
    #sizes = list()
    #phred_score = list()
    #phred_score_transpose = list()
  

    create_transposed_file (inputFile, initial)
    tax_summaries_percentages (inputFile, initial)
