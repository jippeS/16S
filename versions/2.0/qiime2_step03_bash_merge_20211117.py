import os
import pandas as pd
import configparser
import PySimpleGUI as sg
import glob2

config = configparser.ConfigParser()
config.read('/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime_settings.ini')


path = config['qiime']['path']  #op cluster"/export2/home/bgeu"  "/export2/home/bgeu/qiime2_automation/" "/home/pi/"
path_python = config['qiime']['path_python']
path_qiime = config['qiime']['path_qiime']

nodes = config['qiime']['nodes']               #default = "1"
ntasks_per_node = config['qiime']['ntasks_per_node']     #default = "1"
cpus_per_task = config['qiime']['cpus_per_task']      #default = "16" 
qiime_version = config['qiime']['qiime_version']

size_subsample = config['qiime']['size_subsample'] #default 10000
name_sub = int(int(size_subsample)/1000)
fastq_sub = int(int(size_subsample)*4)

#demux
forward_barcodes_file = config['qiime']['forward_barcodes_file']   #rename fle to for example : RBAR_01_20200115@metadata.txt
forward_barcodes_column = config['qiime']['forward_barcodes_column'] #default = "BarcodeSequence"

#cutadapt
forward_primer = config['qiime']['forward_primer']   #beter als ie van de samplesheet wordt ingelezen...... verbeterpuntje
reverse_primer = config['qiime']['reverse_primer']

#DADA2  per dataset parameters bepalen en invoeren!!!!!
trim_forward = config['qiime']['trim_forward']
trim_reverse = config['qiime']['trim_reverse']
length_forward = config['qiime']['length_forward']
length_reverse = config['qiime']['length_reverse']
#trim_quality = "20"

min_depth = config['qiime']['min_depth']
max_depth = config['qiime']['max_depth'] 
sampling_depth = config['qiime']['sampling_depth']

s = " "
#Classifier
path_classifier = config['qiime']['path_classifier']
classifier = config['qiime']['classifier'] #"silva-132-99-nb-classifier.qza" #"/export2/home/bgeu/qiime2_classifiers/NB_classifier_SILVA_132_99_16S_V4-V5_qiime2-2019.10.qza"  qiime2_classifiers

classifier_0 = classifier [:-4]

def create_folder_list (path): 

    folder_names = list()

    os.system("cd " + path[:-1]) # + ";ls *.fastq.gz > " + path_python + "list_fastq_gz_files.txt")

    for entry_name in os.listdir(path[:-1]):
        entry_path = os.path.join(path[:-1], entry_name)
        if os.path.isdir(entry_path):
            entry_name_form = entry_name
            folder_names.append(entry_name_form)
    print(folder_names)
    return (folder_names)   #['Buenano_s1-38_16S_515F926R_20210527', 'temp', 'Buenano_s39-76_16S_515F926R_20210527']

def create_check_box (folder_names):
    checkbox_content = ""
    for folder_name in folder_names:
        folder = str(folder_name)
        checkbox = "[sg.Checkbox('" + folder + "')], "
        checkbox_content = checkbox_content + checkbox
    checkbox_def = checkbox_content  #"["+ checkbox_content[:-2] + "]"
    print(checkbox_def)
    return (checkbox_def)



def qiime2_merge_data_flex_01(checkbox_def): #(folder_names)
        
    
    sg.SetOptions(text_justification='right')

    flags = eval(checkbox_def)


    new_dirname = [[sg.Text('New name', size=(10, 1)), sg.In(size=(30, 1))],]

    layout = [
            
              [sg.Frame('Select folders for merging', flags, font='Helvetica 14', title_color='red')],
              [sg.Frame('Create folder for merged files', new_dirname, title_color='red', font='Helvetica 14')],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Select folders for merging', font=("Helvetica", 12)).Layout(layout)
    button, values = window.Read()
    sg.SetOptions(text_justification='left')
    print(values)
    #print(button, values)
   
    return (values)


def merge_create_new_dir (path, values): #(path, values)
    
    for key, value in values.items():  #for key, value in a_dict.items():
        new_folder_nr = list(values)[-1]
        if key == new_folder_nr:
            new_folder = value
            print('mkdir ', new_folder)
            os.system("cd " + path + ";mkdir " + new_folder )

            break
        else:
            continue

    #print(new_folder)
    return (new_folder)


def merge_search_files (folder_names, values, new_folder): #(path, checkbox_def, values)
    
    s = " "
    i = -1
    for folder in folder_names:
        i += 1

        for key, value in values.items():  #for key, value in a_dict.items():
            if (key == i) and (value == True):
                print('action for ,', i, folder)
                os.system("cd " + path + folder + ";cp " + folder + "_table.qza" + s + path + new_folder + ";cp " + folder + "_representative_sequences.qza" + s + path + new_folder + ";cp " + folder + "@metadata.txt" + s + path + new_folder + ";cp " + "CHECK_" + folder + "_stats.tsv" + s + path + new_folder)
               
                
                break
            else:
                continue

               
    return    


def merge_qiime_metadata_files(path, new_folder):
    metadata_files = glob2.glob(path + new_folder + '/*@metadata.txt')
    #";cp " + folder + "@metadata.txt" + s + path + new_folder + ";cp " + "CHECK_" + folder + "_stats.tsv" + s + path + new_folder)
    merged_metadata_file = path + new_folder + '/' + new_folder + '@merged_metadata.txt'
    merged_metadata = open(merged_metadata_file, 'w+')    
    first_line = False
    for metadata_file in metadata_files:
        metadata = open(metadata_file, 'r')
        print(metadata_file)
        i = 0
        
        for line in metadata:
            if first_line == False: 
                merged_metadata.write(line)
                first_line = True
                i += 1

            elif (first_line == True) and (i >= 1):            
                merged_metadata.write(line)
                first_line = True
                i += 1
                
            else:
                i += 1
                continue
                
    merged_metadata.close()
    return


def merge_qiime_stats_files(path, new_folder):
    stats_files = glob2.glob(path + new_folder + '/*_stats.tsv')
    #";cp " + folder + "@metadata.txt" + s + path + new_folder + ";cp " + "CHECK_" + folder + "_stats.tsv" + s + path + new_folder)
    merged_stats_file = path + new_folder + '/' + new_folder + '@merged_stats.txt'
    merged_stats = open(merged_stats_file, 'w+')    
    first_line = 0
    for stats_file in stats_files:
        stats = open(stats_file, 'r')
        print(stats_file)
        i = 0
        
        for line in stats:
            if first_line == 0: 
                merged_stats.write(line)
                first_line = 1
                i += 1
                
            elif first_line == 1: 
                merged_stats.write(line)
                first_line = 2
                i += 1

            elif (first_line == 2) and (i >= 2):            
                merged_stats.write(line)
                first_line = True
                i += 1
                
            else:
                i += 1
                continue
                
    merged_stats.close()
    return

def step_00_intro_merge (path, nodes, ntasks_per_node, cpus_per_task, new_folder, s, path_qiime, path_python):
    bash_00_intro_merge = ("#!/bin/bash" + "\n"
                           + "#SBATCH --job-name=" + new_folder + "\n"
                           + "#SBATCH --nodes=" + nodes + "\n"
                           + "#SBATCH --ntasks-per-node=" + ntasks_per_node  + "\n"
                           + "#SBATCH --cpus-per-task=" + cpus_per_task + "\n\n"                       
                           + "source activate" + s + path_qiime + "\n\n"
                           + "qiime" + "\n\n"
                           + "cd" + s + path + new_folder + "\n\n"
                           + "cp" + s + path_python + "qiime_settings.ini" + s + path + new_folder + "/qiime_settings.txt" + "\n"
                           + "cp" + s + "-u" + s + path + new_folder + "*_bash_step_03*.sh" + s + path + new_folder + "/" + "\n")

    return bash_00_intro_merge

def step_01_merge_tables (s, path, new_folder, forward_barcodes_file, min_depth, max_depth):

    table_files = glob2.glob( path + new_folder + '/*_table.qza')
    sum_tables = ""
    for table_file in table_files:
        print(table_file)
        sum_tables = sum_tables + s + table_file
    print(sum_tables)    

    bash_01_merge_tables = ("qiime feature-table merge" + s + "\\" + "\n"
                            + "--i-tables" + s + sum_tables + s +  "\\" + "\n"
                            + "--o-merged-table" + s + path + new_folder + "/" + new_folder + "_table.qza" + s +  "\\" + "\n\n")
    return bash_01_merge_tables


#qiime feature-table merge \
#--i-tables /export2/home/microlab/microlab/qiime/illumina_data/Buenano_all_16S_515F926R_20210527/Buenano_s1-38_16S_515F926R_20210527_table.qza /export2/home/microlab/microlab/qiime/illumina_data/Buenano_all_16S_515F926R_20210527/Buenano_s39-76_16S_515F926R_20210527_table.qza \
#--o-merged-table /export2/home/microlab/microlab/qiime/illumina_data/Buenano_all_16S_515F926R_20210527/Buenano_all_16S_515F926R_20210527_table.qza

def step_02_merge_seqs (s, path, new_folder, forward_barcodes_file, min_depth, max_depth):

    seq_files = glob2.glob( path + new_folder + '/*_representative_sequences.qza')
    sum_seqs = ""
    for seq_file in seq_files:
        print(seq_file)
        sum_seqs = sum_seqs + s + seq_file
    print(sum_seqs)    

    bash_02_merge_seqs = ("qiime feature-table merge-seqs" + s + "\\" + "\n"
                            + "--i-data" + s + sum_seqs + s +  "\\" + "\n"
                            + "--o-merged-data" + s + path + new_folder + "/" + new_folder + "_representative_sequences.qza" + s +  "\\" + "\n\n")
    return bash_02_merge_seqs

#qiime feature-table merge-seqs \
#--i-data /export2/home/microlab/microlab/qiime/illumina_data/Buenano_all_16S_515F926R_20210527/Buenano_s1-38_16S_515F926R_20210527_representative_sequences.qza /export2/home/microlab/microlab/qiime/illumina_data/Buenano_all_16S_515F926R_20210527/Buenano_s39-76_16S_515F926R_20210527_representative_sequences.qza \
#--o-merged-data /export2/home/microlab/microlab/qiime/illumina_data/Buenano_all_16S_515F926R_20210527/Buenano_all_16S_515F926R_20210527_representative_sequences.qza

def step_03_feature_table_sum (s, new_folder, path):
    bash_03_feature_table_sum = ("qiime feature-table summarize" + s + "\\" + "\n"
                                 + "--i-table" + s + path + new_folder + "/" + new_folder + "_table.qza" + s + "\\" + "\n"
                                 + "--m-sample-metadata-file" + s + path + new_folder + "/" + new_folder + "@merged_metadata.txt" + s + "\\" + "\n"
                                 + "--o-visualization" + s + path + new_folder + "/" + new_folder + "_table.qzv" + "\n")
    return bash_03_feature_table_sum



# view generated feature table
#qiime feature-table summarize \
#  --i-table table.qza \
#  --m-sample-metadata-file ~/QIIME2_workshop/metadata.txt
#  --o-visualization table.qzv
  
#qiime tools view table.qzv


def step_04_representative_seqs (s, path, new_folder): 
    bash_04_representative_seqs = ("qiime feature-table tabulate-seqs" + s + "\\" + "\n"
                                   + "--i-data" + s + path + new_folder + "/" + new_folder + "_representative_sequences.qza" + s + "\\" + "\n"
                                   + "--o-visualization" + s + path + new_folder + "/" + new_folder + "_representative_sequences.qzv" + "\n")
                                   #+ "cd.." + "\n")
    return bash_04_representative_seqs

# view representative sequences for each ASV
#qiime feature-table tabulate-seqs \
# --i-data representative_sequences.qza \
#  --o-visualization representative_sequences.qzv
#qiime tools view representative_sequences.qzv

def step_05_align_mafft (s, path, new_folder, cpus_per_task):
    bash_05_align_mafft = ("qiime alignment mafft" + s + "\\" + "\n"
                           + "--i-sequences" + s + path + new_folder + "/" + new_folder + "_representative_sequences.qza" + s + "\\" + "\n"
                           + "--o-alignment" + s + path + new_folder + "/" + new_folder + "_aligned-rep-seqs.qza" + s + "\\" + "\n"
                           + "--p-n-threads" + s + cpus_per_task + s + "\n")
    return bash_05_align_mafft

#qiime alignment mafft \
#  --i-sequences DADA2_out/representative_sequences.qza \
#  --o-alignment aligned-rep-seqs.qza \
#  --p-n-threads 16


def step_06_align_mask (s, path, new_folder):
    bash_06_align_mask = ("qiime alignment mask" + s + "\\" + "\n"
                          + "--i-alignment" + s + path + new_folder + "/" + new_folder + "_aligned-rep-seqs.qza" + s + "\\" + "\n"
                          + "--o-masked-alignment" + s + path + new_folder + "/" + new_folder + "_masked_aligned-rep-seqs.qza" + "\n")
    return bash_06_align_mask


#qiime alignment mask \
#  --i-alignment aligned-rep-seqs.qza \
#  --o-masked-alignment masked_aligned-rep-seqs.qza

def step_07_phyl_fast (s, path, new_folder, cpus_per_task):
    bash_07_phyl_fast = ("qiime phylogeny fasttree" + s + "\\" + "\n"
                         + "--i-alignment" + s + path + new_folder + "/" + new_folder + "_masked_aligned-rep-seqs.qza" + s + "\\" + "\n"
                         + "--o-tree" + s + path + new_folder + "/" + new_folder + "_unrooted-tree.qza" + s + "\\" + "\n"
                         + "--p-n-threads" + s + cpus_per_task + "\n")
    return bash_07_phyl_fast

#qiime phylogeny fasttree \
#  --i-alignment masked_aligned-rep-seqs.qza \
#  --o-tree unrooted-tree.qza \
#  --p-n-threads 16


def step_08_phyl_mid (s, path, new_folder):
    bash_08_phyl_mid = ("qiime phylogeny midpoint-root" + s + "\\" + "\n"
                          + "--i-tree" + s + path + new_folder + "/" + new_folder + "_unrooted-tree.qza" + s + "\\" + "\n"
                          + "--o-rooted-tree" + s + path + new_folder + "/" + new_folder + "_rooted-tree.qza" + "\n")
    return bash_08_phyl_mid
  
#qiime phylogeny midpoint-root \
#  --i-tree unrooted-tree.qza \
#  --o-rooted-tree rooted-tree.qza

def step_09_feature_class (s, path, new_folder, classifier, cpus_per_task, path_classifier):
    bash_09_feature_class = ("qiime feature-classifier classify-sklearn" + s + "\\" + "\n"
                             + "--i-classifier" + s + path_classifier + classifier + s + "\\" + "\n"
                             + "--i-reads" + s + path + new_folder + "/" + new_folder + "_representative_sequences.qza" + s + "\\" + "\n"
                             + "--o-classification" + s + path + new_folder + "/" + new_folder + "_taxonomy_" + classifier + s + "\\" + "\n"
                             + "--p-n-jobs" + s + cpus_per_task + "\n")
    return bash_09_feature_class

#qiime feature-classifier classify-sklearn \
#  --i-classifier NB_classifier_SILVA_132_99_16S_V4-V5.qza \
#  --i-reads DADA2_out/representative_sequences.qza \
#  --o-classification taxonomy_Silva132_99-515F-926R_classifier.qza \
#  --p-n-jobs 16

def step_10_metadata_tab (s, path, new_folder, classifier, classifier_0 ):
    bash_10_metadata_tab = ("qiime metadata tabulate" + s + "\\" + "\n"
                            + "--m-input-file" + s + path + new_folder + "/" + new_folder + "_taxonomy_" + classifier + s + "\\" + "\n"
                            + "--o-visualization" + s + path + new_folder + "/" + new_folder + "_taxonomy_" + classifier_0 + ".qzv" + "\n")
                            #+ "mkdir" + s + "/" + identifier + "_output_files" + "\n\n")
    return bash_10_metadata_tab


#qiime metadata tabulate \
#  --m-input-file taxonomy_SILVA_132_99_16S_V4-V5.qza \
#  --o-visualization taxonomy_SILVA_132_99_16S_V4-V5.qzv


def step_11_export_repr_seq_fasta (s, path, new_folder):
    bash_11_export_repr_seq_fasta = ("qiime tools export" + s + "\\" + "\n"
                                     + "--input-path" + s + path + new_folder + "/" + new_folder + "_representative_sequences.qza" + s + "\\" + "\n"
                                     + "--output-path" + s + path + new_folder + "\n")
    return bash_11_export_repr_seq_fasta

# export representative sequences as a .fasta file
#qiime tools export \
#  --input-path DADA2_out/representative_sequences.qza \
#  --output-path output_files/rep-seqs

def step_12_export_feat_tbl_biom (s, path, new_folder):
    bash_12_export_feat_tbl_biom = ("qiime tools export" + s + "\\" + "\n"
                                    + "--input-path" + s + path + new_folder + "/" + new_folder + "_table.qza" + s + "\\" + "\n"
                                    + "--output-path" + s + path + new_folder + "\n")


    return bash_12_export_feat_tbl_biom

# export feature table as .biom file
#qiime tools export \
#  --input-path DADA2_out/table.qza \
#  --output-path output_files/exported-table

def step_13_export_phyl_newick (s, path, new_folder):
    bash_13_export_phyl_newick = ("qiime tools export" + s + "\\" + "\n"
                                    + "--input-path" + s + path + new_folder + "/" + new_folder + "_rooted-tree.qza" + s + "\\" + "\n"
                                    + "--output-path" + s + path + new_folder +  "\n")

    return bash_13_export_phyl_newick

# export phylogeny as .nwk tree file in Newick format
#qiime tools export \
#  --input-path rooted-tree.qza \
#  --output-path output_files/exported-tree

def step_14_export_taxonomy_tsv (s, path, new_folder, classifier):
    bash_14_export_taxonomy_tsv = ("qiime tools export" + s + "\\" + "\n"
                                    + "--input-path" + s + path + new_folder + "/" + new_folder + "_taxonomy_" + classifier + s + "\\" + "\n"
                                    + "--output-path" + s + path + new_folder + "/" + "\n")

    return bash_14_export_taxonomy_tsv



def step_15_alpha_rarefaction (s, path, new_folder, min_depth, max_depth):
    bash_15_alpha_rarefaction = ("qiime diversity alpha-rarefaction" + s + "\\" + "\n"
                                 + "--i-table" + s + path + new_folder + "/" + new_folder + "_table.qza" + s +  "\\" + "\n"
                                 + "--m-metadata-file" + s + path + new_folder + "/" + new_folder + "@merged_metadata.txt" + s + "\\" + "\n"
                                 + "--o-visualization" + s + path + new_folder + "/" + new_folder + "_alpha_rarefaction_curves.qzv" + s + "\\" + "\n"
                                 + "--p-min-depth" + s + min_depth + s + "\\" + "\n"
                                 + "--p-max-depth" + s + max_depth + "\n\n")
    return bash_15_alpha_rarefaction




#qiime diversity alpha-rarefaction \
#  --i-table DADA2_out/table.qza \
#  --m-metadata-file metadata.txt \
#  --o-visualization alpha_rarefaction_curves.qzv \
#  --p-min-depth 10 \
#  --p-max-depth xxx


def step_16_microbial_diversity (s, path, new_folder, forward_barcodes_file, sampling_depth):
    bash_16_microbial_diversity = ("qiime diversity core-metrics-phylogenetic" + s + "\\" + "\n"
                                   + "--i-table" + s + path + new_folder + "/" + new_folder + "_table.qza" + s +  "\\" + "\n"
                                   + "--i-phylogeny" + s + path + new_folder + "/" + new_folder + "_rooted-tree.qza" + s + "\\" + "\n"
                                   + "--m-metadata-file" + s + path + new_folder + "/" + new_folder + "@merged_metadata.txt" + s + "\\" + "\n"
                                   + "--p-sampling-depth" + s + sampling_depth + s + "\\" + "\n"
                                   + "--output-dir" + s + path + new_folder + "/" + new_folder + "_microbial-diversity-results" + "\n\n")
    return bash_16_microbial_diversity
                                   

#qiime diversity core-metrics-phylogenetic \
#  --i-table DADA2_out/table.qza \
#  --i-phylogeny rooted-tree.qza \
#  --m-metadata-file metadata.txt \
#  --p-sampling-depth 260 \
#  --output-dir microbial-diversity-results


def step_17_taxa_barplot (s, path, new_folder, forward_barcodes_file, classifier):
    bash_17_taxa_barplot = ("qiime taxa barplot" + s + "\\" + "\n"
                            + "--i-table" + s + path + new_folder + "/" + new_folder + "_table.qza" + s +  "\\" + "\n"
                            + "--i-taxonomy" + s + path + new_folder + "/" + new_folder + "_taxonomy_" + classifier + s + "\\" + "\n"
                            + "--m-metadata-file" + s + path + new_folder + "/" + new_folder + "@merged_metadata.txt" + s + "\\" + "\n"
                            + "--o-visualization" + s + path + new_folder + "/" + new_folder + "_taxa_barplot.qzv" + "\n\n")
    return bash_17_taxa_barplot

#qiime taxa barplot \
  #--i-table DADA2_out/table.qza \
  #--i-taxonomy taxonomy_Silva132_99-515F-926R_classifier_qiime2-2019.10.qza \
  #--m-metadata-file metadata.txt \
  #--o-visualization taxa_barplot.qzv

#qiime tools view taxa_barplot.qzv

def step_18_taxa_relative_amounts (s, path, new_folder, path_python): 

    bash_18_taxa_relative_amounts = ("mkdir" + s + path + new_folder + "/" + new_folder + "_taxa_absolute_relative" + "\n" 
                                    + "unzip" + s + path + new_folder + "/" + new_folder + "_taxa_barplot.qzv" + s + "-d" + s + path + new_folder + "/" + new_folder + "_taxa_absolute_relative" + "\n"
                                    #+ "cd" + + s + path + identifier + "/" + "\n"  
                                      #echo MAC_CNR1M12_R26RNA > /export3/home/bgeu/transcriptomics/fastq_demux/MAC_CNR1M12_R26RNA/MAC_CNR1M12_R26RNA.id


                                     + "echo" + s + new_folder + s + ">" + s + path + new_folder + "/" + new_folder + "_taxa_absolute_relative" + "/" + new_folder + ".id" + "\n"
                                    + "find" + s + path + new_folder + s + "-type f -name 'level-*.csv' -exec sh -c" + s + "'for arg do cp --" + s + '"$arg"' + s
                                    + '"' + path + new_folder + "/" + new_folder + "_taxa_absolute_relative/" + '"' + "; done' _ {} +" + "\n"
                                     + "cd" + s + path + new_folder + "/" + new_folder + "_taxa_absolute_relative/" + "\n"
                                     + "ls" + s + "level-*.csv > list_csv_files.txt" + "\n" 
                                    + "cp" + s + path_python + "transpose_csv_files.py" + s + path + new_folder + "/" + new_folder + "_taxa_absolute_relative/" + "\n"
                                    
                                      + "python3.6" + s + path + new_folder + "/" + new_folder + "_taxa_absolute_relative/transpose_csv_files.py" + "\n" )                                   
                                      #+ "find" + s + path + identifier + s + "-type f -name 'reverse-seven-number-summaries.csv' -exec sh -c" + s + "'for arg do cp --" + s + '"$arg"' + s
                                      #+ '"' + path + identifier + "/" + identifier + "_reverse-seven-number-summaries.csv" + '"' + "; done' _ {} +" + "\n"
                                      # + "cp" + s + path + "quality_scores_datasets.txt" + s + path + identifier + "/" + identifier + "_quality_scores_datasets.txt" + "\n"
                                      #+ "unzip" + s + path + identifier + "/" + identifier + "_denoising_stats.qza" + s + "-d" + s + path + identifier + "\n"
                                      #+ "find" + s + path + identifier + s + "-type f -name 'stats.tsv' -exec sh -c" + s + "'for arg do cp --" + s + '"$arg"' + s
                                    #+ '"' + path + identifier + "/" + "CHECK_" + identifier + "_stats.tsv" + '"' + "; done' _ {} +" + "\n")

                                     
    
    return bash_18_taxa_relative_amounts

folder_names = create_folder_list(path)
checkbox_def = create_check_box(folder_names)
values = qiime2_merge_data_flex_01(checkbox_def)
new_folder = merge_create_new_dir (path, values)
merge_search_files (folder_names, values, new_folder)
merge_qiime_metadata_files(path, new_folder)
merge_qiime_stats_files(path, new_folder)

bash_00_intro_merge = step_00_intro_merge(path, nodes, ntasks_per_node, cpus_per_task, new_folder, s, path_qiime, path_python)
bash_01_merge_tables = step_01_merge_tables(s, path, new_folder, forward_barcodes_file, min_depth, max_depth)
bash_02_merge_seqs = step_02_merge_seqs(s, path, new_folder, forward_barcodes_file, min_depth, max_depth)
bash_03_feature_table_sum = step_03_feature_table_sum(s, new_folder, path)
bash_04_representative_seqs = step_04_representative_seqs(s, path, new_folder)
bash_05_align_mafft = step_05_align_mafft(s, path, new_folder, cpus_per_task)
bash_06_align_mask = step_06_align_mask(s, path, new_folder)
bash_07_phyl_fast = step_07_phyl_fast(s, path, new_folder, cpus_per_task)
bash_08_phyl_mid = step_08_phyl_mid(s, path, new_folder)
bash_09_feature_class = step_09_feature_class(s, path, new_folder, classifier, cpus_per_task, path_classifier)
bash_10_metadata_tab = step_10_metadata_tab(s, path, new_folder, classifier, classifier_0 )
bash_11_export_repr_seq_fasta = step_11_export_repr_seq_fasta(s, path, new_folder)
bash_12_export_feat_tbl_biom = step_12_export_feat_tbl_biom(s, path, new_folder)
bash_13_export_phyl_newick = step_13_export_phyl_newick(s, path, new_folder)
bash_14_export_taxonomy_tsv = step_14_export_taxonomy_tsv(s, path, new_folder, classifier)
bash_15_alpha_rarefaction = step_15_alpha_rarefaction(s, path, new_folder, min_depth, max_depth)
bash_16_microbial_diversity = step_16_microbial_diversity(s, path, new_folder, forward_barcodes_file, sampling_depth)
bash_17_taxa_barplot = step_17_taxa_barplot(s, path, new_folder, forward_barcodes_file, classifier)
bash_18_taxa_relative_amounts = step_18_taxa_relative_amounts(s, path, new_folder, path_python) 

sbatchfile_merged = (path + new_folder + "/" + new_folder + "_bash_merged_qiime_scripts.sh") #(identifier + "_bash_step_02_qiime_graphs.sh")
sbatch_merged = open(sbatchfile_merged , mode='wb+', newline = None)

text_to_write_merged = ( bash_00_intro_merge + "\n" + bash_01_merge_tables + "\n" +  bash_02_merge_seqs + "\n"
                       + bash_03_feature_table_sum + "\n" + bash_04_representative_seqs + "\n" + bash_05_align_mafft + "\n"
                       + bash_06_align_mask + "\n" + bash_07_phyl_fast + "\n" + bash_08_phyl_mid + "\n"
                       + bash_09_feature_class + "\n" + bash_10_metadata_tab + "\n" + bash_11_export_repr_seq_fasta + "\n"
                       + bash_12_export_feat_tbl_biom + "\n" + bash_13_export_phyl_newick  + "\n" + bash_14_export_taxonomy_tsv + "\n"
                       + bash_15_alpha_rarefaction + "\n" + bash_16_microbial_diversity + "\n" + bash_17_taxa_barplot + "\n"
                       + bash_18_taxa_relative_amounts + "\n" + "source deactivate" )


sbatch_merged.write(bytes(text_to_write_merged, "UTF-8"))

sbatch_merged.close()

print(new_folder, " done")
print("qiime2_merge_bash_qiime2 script created")




