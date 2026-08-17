import pandas as pd
import csv
import glob2
from Bio import SeqIO
from Bio.Seq import Seq
import numpy as np
import re



inputFile = "level-7.csv"

#inputFile = 'level-3.csv'

search_list = ['metagenome','Ambiguous','uncultured bacterium','uncultured soil bacterium']

def create_transposed_file (inputFile, initial):

    outputFile = initial + "_transpose_" + inputFile

    output = open(outputFile, 'w+')

    
    data = pd.read_csv(inputFile, sep=",") #pd.read_csv(input_unknowns_file, sep="\t", names=col_Names)

    transposed_data = data.transpose() #transposed_data = data.set_index('Description').transpose()

    transposed_data.to_csv(output, sep='\t', decimal='.', line_terminator = '\r', index=True)
    

    return

def tax_summaries_percentages_OLD (inputFile, initial):  #OLD SCRIPT!!!!!

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


def match_tax_name(tax_name, search_list):

    match = 0
    for item in search_list:
        #print(item, tax_name)
        #regex = re.compile(item)
        #print(regex)
        match_count = re.findall("%s" % item, tax_name) #re.findall(re.escape(item), tax_name)#re.findall("%s" % item, tax_name) #len(regex.findall(tax_name))
        #print(match_count)
        match = match + len(match_count)
    total_match = int(match)
    return total_match



def write_tax_lines_level_0_7 (line, tax_nr, new_tax_line, abs_data, output_d0, output_d1, output_d2, output_d3, output_d4, output_d5, output_d6):

    if tax_nr == 0:
        line_complete = new_tax_line + '\t' + abs_data
        output_d0.write(line_complete)

    elif tax_nr == 1:
        line_complete = new_tax_line + '\t' + abs_data
        output_d1.write(line_complete)

    elif tax_nr == 2:
        line_complete = new_tax_line + '\t' + abs_data
        output_d2.write(line_complete)

    elif tax_nr == 3:
        line_complete = new_tax_line + '\t' + abs_data
        output_d3.write(line_complete)

    elif tax_nr == 4:
        line_complete = new_tax_line + '\t' + abs_data
        output_d4.write(line_complete)

    elif tax_nr == 5:
        line_complete = new_tax_line + '\t' + abs_data
        output_d5.write(line_complete)

    elif tax_nr == 6:
        line_complete = new_tax_line + '\t' + abs_data
        output_d6.write(line_complete)
        print('ORGINAL LINE  ' , line)
        print(line_complete)
    else:
        exit
        

    return




def tax_add_tax_info_to_level_7 (inputFile, initial):#(inputFile, initial)

    #  	0	1	2	3	4	5	6	7	8	9	10	11
    #index	JPER.001	JPER.002	JPER.003	JPER.004	JPER.005	JPER.006	JPER.007	JPER.008	JPER.009	JPER.010	JPER.011	JPER.BLANK
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Corynebacteriaceae;D_5__Corynebacterium 1;D_6__uncultured bacterium	0.0	0.0	9.0	121.0	0.0	0.0	3.0	0.0	0.0	0.0	0.0	0.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Corynebacteriaceae;D_5__Corynebacterium 1;__	72.0	29.0	0.0	441.0	51.0	143.0	29.0	48.0	14.0	1105.0	0.0	0.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Corynebacteriaceae;D_5__Corynebacterium;Ambiguous_taxa	0.0	0.0	0.0	235.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Corynebacteriaceae;D_5__Corynebacterium;D_6__Corynebacterium glucuronolyticum	20.0	6.0	0.0	373.0	11.0	62.0	9.0	179.0	0.0	0.0	0.0	0.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Corynebacteriaceae;D_5__Corynebacterium;__	0.0	0.0	0.0	151.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	7.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Corynebacteriaceae;D_5__Lawsonella;__	128.0	20.0	19.0	1420.0	30.0	242.0	51.0	548.0	17.0	474.0	52.0	23.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Corynebacteriaceae;__;__	0.0	0.0	0.0	0.0	5.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Mycobacteriaceae;D_5__Mycobacterium;D_6__Mycobacterium abscessus subsp. abscessus	0.0	0.0	0.0	0.0	16.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Nocardiaceae;D_5__Gordonia;__	0.0	0.0	0.0	0.0	15.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Nocardiaceae;D_5__Nocardia;__	0.0	0.0	3.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
    #D_0__Bacteria;D_1__Actinobacteria;D_2__Actinobacteria;D_3__Corynebacteriales;D_4__Nocardiaceae;D_5__Rhodococcus;__	78.0	16.0	15.0	1395.0	141.0	402.0	37.0	0.0	23.0	4.0	18.0	0.0

    inputFile2 = initial + "_transpose_" + inputFile
    data = open(inputFile2, 'r')

    outputFile_d0 = initial + "_transpose_D0_completed_" + inputFile[:-5] + '1.txt'
    output_d0 = open(outputFile_d0, 'w+')

    outputFile_d1 = initial + "_transpose_D1_completed_" + inputFile[:-5] + '2.txt'
    output_d1 = open(outputFile_d1, 'w+')

    outputFile_d2 = initial + "_transpose_D2_completed_" + inputFile[:-5] + '3.txt'
    output_d2 = open(outputFile_d2, 'w+')

    outputFile_d3 = initial + "_transpose_D3_completed_" + inputFile[:-5] + '4.txt'
    output_d3 = open(outputFile_d3, 'w+')

    outputFile_d4 = initial + "_transpose_D4_completed_" + inputFile[:-5] + '5.txt'
    output_d4 = open(outputFile_d4, 'w+')

    outputFile_d5 = initial + "_transpose_D5_completed_" + inputFile[:-5] + '6.txt'
    output_d5 = open(outputFile_d5, 'w+')
    
    outputFile_d6 = initial + "_transpose_D6_completed_" + inputFile[:-5] + '7.txt'
    output_d6 = open(outputFile_d6, 'w+')

    

    #list_forbidden_words = 

    for line in data: #D_0__Bacteria;D_1__Synerg     Description	JPER_001	JPER_002	JPER_003
        #print(line)
        if "Description\t" in line:
            output_d0.write(line)
            output_d1.write(line)
            output_d2.write(line)
            output_d3.write(line)
            output_d4.write(line)
            output_d5.write(line)
            output_d6.write(line)
            data.close()
            break
        else:
            continue

    data1 = open(inputFile2, 'r')
    for line in data1:
        info_tax = 'complete'
        if "D_0__" in line:
            line0 = line.split('\t', 1)
            tax0 = line0[0]
            abs_data = line0[1] #78.0	16.0	15.0	1395.0	141.0	402.0	37.0	0.0	23.0	4.0	18.0	0.0
            tax1 = tax0.split(';')
            tax_nr = -1
            new_tax_line = ''
            last_tax_item = ''
            last_tax_name = ''
            
            for tax_item in tax1:
                tax_nr += 1
                tax_item0 = tax_item.split('_')
                #print(line)
                if ((tax_item0[0] == 'D') and (info_tax == 'complete')) and (str(tax_item0[3]) != 'uncultured'):
                    tax_name = str(tax_item0[3])
                    total_match = match_tax_name(tax_name, search_list)
                    #print(total_match, tax_name)
                    if (total_match == 0):                    
                        last_tax_name = str(tax_item0[3])
                        new_tax_line = new_tax_line + ('D_' + str(tax_nr) + '__' + last_tax_name + ';')
                        #print(new_tax_line)
                        write_tax_lines_level_0_7 (line, tax_nr, new_tax_line, abs_data, output_d0, output_d1, output_d2, output_d3, output_d4, output_d5, output_d6)
                    else:
                        new_tax_line = new_tax_line + ('D_' + str(tax_nr) + '__' + last_tax_name + ' unclassified;')
                        info_tax = 'incomplete'
                        write_tax_lines_level_0_7 (line, tax_nr, new_tax_line, abs_data, output_d0, output_d1, output_d2, output_d3, output_d4, output_d5, output_d6)
                         

                else:
                    new_tax_line = new_tax_line + ('D_' + str(tax_nr) + '__' + last_tax_name + ' unclassified;')
                    info_tax = 'incomplete'
                    write_tax_lines_level_0_7 (line, tax_nr, new_tax_line, abs_data, output_d0, output_d1, output_d2, output_d3, output_d4, output_d5, output_d6)
                    
        else:
            continue

    output_d0.close()
    output_d1.close()
    output_d2.close()
    output_d3.close()
    output_d4.close()
    output_d5.close()
    output_d6.close()
    
    return

def tax_summaries_percentages (initial):

    input_completed_files = glob2.glob(initial + "_transpose_D*_completed_" + '*.txt')
    for input_completed_file in input_completed_files:
        print(str(input_completed_file))
        input_completed = open(input_completed_file, 'r')
        outputFile_abs = (input_completed_file[:-4] + '_absolute.txt') #"test_01_groupby_JPER_Q13340_16S_515F926R_20210311_transpose_D6_completed_level-7.txt"
        output_abs = open(outputFile_abs, 'w+')        
        outputFile_rel = (input_completed_file[:-4] + '_relative.txt') #"test_01_groupby_JPER_Q13340_16S_515F926R_20210311_transpose_D6_completed_level-7.txt"
        output_rel = open(outputFile_rel, 'w+')      

        data = pd.read_csv(input_completed, sep="\t")


        data_abs = data.groupby('Description').sum()

        data_abs.to_csv(output_abs, sep='\t', decimal='.', line_terminator = '\r', index=True)
        #output_abs.close()

        #list_oligo_count = data.groupby(['primer_name','sample','type_analysis','project']).agg({'primer_name': 'count'})


        #groupby_data.to_csv(output2, sep='\t', decimal='.', line_terminator = '\r', index=True) 

        #outputFile3 = "test_01_percentages_JPER_Q13340_16S_515F926R_20210311_transpose_D6_completed_level-7.txt"
        #output3 = open(outputFile3, 'w+')
        #data1 = pd.read_csv("test_01_groupby_JPER_Q13340_16S_515F926R_20210311_transpose_D6_completed_level-7.txt", sep="\t")

        data_num = data_abs.select_dtypes(include=[np.number])



        data_num_pct = data_num/data_num[data_num.columns].sum()*100

        data_abs[data_num_pct.columns] = data_num_pct
        data_pct = data_abs


        data_pct.to_csv(output_rel, sep='\t', decimal='.', line_terminator = '\r', index=True) 


        print(list(data))
        print (data)
        print (data_abs)
        print(data_num)
        print(data_num_pct)
        print(data_pct)
        output_abs.close()
        output_rel.close()
        
    return        







#input rel_perc#    initial + "_transpose_D0_completed_" + inputFile[:-5] + '1.txt'
#inputFile2 = "JPER_Q13340_16S_515F926R_20210311_transpose_D6_completed_level-7.txt"  #initial + "JPER_Q13340_16S_515F926R_20210311_transpose_D6_completed_level-7.txt"
#data1 = open(inputFile2, 'r')
    
#outputFile2 = "test_01_groupby_JPER_Q13340_16S_515F926R_20210311_transpose_D6_completed_level-7.txt"
#output2 = open(outputFile2, 'w+')

#Description	JPER_001	JPER_002	JPER_003	JPER_004	JPER_005	JPER_006	JPER_007	JPER_008	JPER_009	JPER_010	JPER_011	JPER_BLANK
#D_0__Archaea;D_1__Euryarchaeota;D_2__Methanobacteria;D_3__Methanobacteriales;D_4__Methanobacteriaceae;D_5__Methanobrevibacter;D_6__Methanobrevibacter arboriphilus;	13.0	22.0	21.0	0.0	5.0	0.0	14.0	0.0	50.0	0.0	38.0	0.0



initial_list = glob2.glob("*.id")
print(str(initial_list))
initial0 = initial_list
print("NAAM_FILE  @@@@", initial0)     
initial1 = str(initial0)    
print(initial1)
initial = initial1 [2:-5]
print(initial)

 

create_transposed_file (inputFile, initial)         #step1
tax_add_tax_info_to_level_7(inputFile, initial)   #step2
tax_summaries_percentages (initial)      #step3

