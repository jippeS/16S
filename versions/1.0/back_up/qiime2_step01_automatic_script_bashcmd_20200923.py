import os
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('/export2/home/microlab/microlab/python_scripts/qiime/qiime_settings.ini')


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


#Classifier
path_classifier = config['qiime']['path_classifier']
classifier = config['qiime']['classifier'] #"silva-132-99-nb-classifier.qza" #"/export2/home/bgeu/qiime2_classifiers/NB_classifier_SILVA_132_99_16S_V4-V5_qiime2-2019.10.qza"  qiime2_classifiers


#############################################################################################################################################

#os.system("python3.7 /export2/home/bgeu/python_scripts/qiime2/qiime2_subsampling_10kseq.py")

#os.system("python3.7 /export2/home/bgeu/python_scripts/qiime2/qiime2_nested_list_transpose.py")

s = " "

os.system("ls *.fastq.gz > list_fastq_gz_files.txt")  #"ls [A-Z]*.fastq.gz > list_fastq_gz_files.txt;ls [0-9]*.fastq.gz > subset_fastq_gz_files.txt")

inputfiles = open("list_fastq_gz_files.txt" , "r") 

classifier_0 = classifier [:-4]


def step_00_intro_sub_quality (path, nodes, ntasks_per_node, cpus_per_task, identifier, s, qiime_version, path_qiime, path_python, forward_barcodes_file, fastq_sub, name_sub):
    bash_00_intro_sub_quality = ("#!/bin/bash" + "\n"
                       + "#SBATCH --job-name=" + identifier + "\n"
                       + "#SBATCH --nodes=" + nodes + "\n"
                       + "#SBATCH --ntasks-per-node=" + ntasks_per_node  + "\n"
                       + "#SBATCH --cpus-per-task=" + cpus_per_task + "\n\n"                       
                       + "source activate" + s + path_qiime + "\n\n" #"source activate" + s + path_qiime + "\n\n"
                       + "cd" + s + path[:-1] + "\n\n"
                       + "ls [A-Z]*.fastq.gz > list_fastq_gz_files.txt" + "\n\n"
                       + "mkdir -p" + s + path + "temp" + "\n"   # "mkdir -p temp" + "\n"
                       + "export TMPDIR=" + path + "temp" + "\n\n"
                       + "mkdir -p" + s + identifier  + "\n\n" #"mkdir -p" + s + path + identifier + "\n\n"
                       + "mkdir -p" + s + identifier  + "/raw_data" + "\n\n"
                       #+ "mkdir -p" + s + identifier  + "/raw_data/subsample" + "\n\n"
                       + "qiime" + "\n\n"
                       + "cp" + s + "-u" + s + identifier + "@*_R1_*.fastq.gz" + s + path + identifier + "/" + "\n"
                       + "cp" + s + "-u" + s + identifier + "@*_R2_*.fastq.gz" + s + path + identifier + "/" + "\n"
                       + "cp" + s + "-u" + s + identifier + "*_bash_step_*.sh" + s + path + identifier + "/" + "\n" 
                       + "gunzip" + s + "-k" + s + path + identifier + "/"  + identifier + "@*_R1_*.fastq.gz" + "\n"
                       + "gunzip" + s + "-k" + s + path + identifier + "/"  + identifier + "@*_R2_*.fastq.gz" + "\n"
                       + "cp" + s + path_python + "qiime_pre_demux.py" + s + path + identifier + "/" + "\n"
                       + "cp" + s + path_python + "qiime2_subsampling_quality_check.py" + s + path + identifier + "/" + "\n"     
                       + "cp" + s + identifier + "@" + forward_barcodes_file + s + path + identifier + "/" + "\n"
                       + "cd" + s + path + identifier + "\n"                      
                       + "python3.6" + s + "qiime_pre_demux.py" + "\n"
                       + "cd" + s + path + identifier + "/raw_data/" + "\n"
                       + "chmod -R 777 *.fastq" + "\n"                       
                       + "head -" + str(fastq_sub) + s + path + identifier + "/raw_data/forward.fastq" + s + ">" + s + path + identifier + "/" + str(name_sub) + "kseq-" + identifier + "@sub_R1_sample.fastq" + "\n"  # + ";iconv -f us-ascii -t utf-8 "  + path + outputfile_10kseq + " > "  + outputfile_10kseq[:-6] + "_utf8.fastq" )
                       + "head -" + str(fastq_sub) + s + path + identifier + "/raw_data/reverse.fastq" + s + ">" + s + path + identifier + "/" + str(name_sub) + "kseq-" + identifier + "@sub_R2_sample.fastq" + "\n"  # + ";iconv -f us-ascii -t utf-8 "  + path + outputfile_10kseq + " > "  + outputfile_10kseq[:-6] + "_utf8.fastq" )
                       + "gzip -k" +  s + path + identifier + "/" + str(name_sub) + "kseq-" + identifier + "@sub_R1_sample.fastq" + "\n"  # + ";iconv -f us-ascii -t utf-8 "  + path + outputfile_10kseq + " > "  + outputfile_10kseq[:-6] + "_utf8.fastq" )
                       + "gzip -k" +  s + path + identifier + "/" + str(name_sub) + "kseq-" + identifier + "@sub_R2_sample.fastq" + "\n"  # + ";iconv -f us-ascii -t utf-8 "  + path + outputfile_10kseq + " > "  + outputfile_10kseq[:-6] + "_utf8.fastq" )
                       #+ "cp" + s + "-u" + s + path + identifier + "/" + str(name_sub) + "kseq-" + identifier + "@sub_R1_sample.fastq.gz" + s + path + identifier + "/raw_data/subsample/forward.fastq.gz" + "\n"  # + ";iconv -f us-ascii -t utf-8 "  + path + outputfile_10kseq + " > "  + outputfile_10kseq[:-6] + "_utf8.fastq" )
                       #+ "cp" + s + "-u" + s + path + identifier + "/" + str(name_sub) + "kseq-" + identifier + "@sub_R2_sample.fastq.gz" + s + path + identifier + "/raw_data/subsample/reverse.fastq.gz" + "\n"  # + ";iconv -f us-ascii -t utf-8 "  + path + outputfile_10kseq + " > "  + outputfile_10kseq[:-6] + "_utf8.fastq" )

                       + "cp" + s + "-u" + s + path + identifier + "/" + identifier + "@metadata.txt " + path + str(name_sub) + "kseq-" + identifier + "@metadata.txt" + "\n"
                       + "cp" + s + "-u" + s + path + identifier + "/" + "*kseq-" + identifier + "@*" + s + path + "\n" # + ";iconv -f us-ascii -t utf-8 "  + path + outputfile_10kseq + " > "  + outputfile_10kseq[:-6] + "_utf8.fastq" )
                       + "gzip *.fastq" + "\n"
                       + "cp" + s + "-u" + s + path + identifier + "/raw_data/forward.fastq.gz" + s + path + identifier + "/" + identifier + "@clean_R1_seq.fastq.gz" + "\n"
                       + "cp" + s + "-u" + s + path + identifier + "/raw_data/reverse.fastq.gz" + s + path + identifier + "/" + identifier + "@clean_R2_seq.fastq.gz" + "\n"
                       + "cd" + s + path + identifier + "\n"
                       + "chmod -R 777 *.fastq.gz" + "\n"
                       + "python3.6 qiime2_subsampling_quality_check.py" + "\n"
                       + "cd" + s + path[:-1] + "\n\n")

    return bash_00_intro_sub_quality

def step_00_intro_qiime_scripts (path, nodes, ntasks_per_node, cpus_per_task, identifier, s, qiime_version, path_qiime): #old
    bash_00_intro_qiime_scripts = ("#!/bin/bash" + "\n"
                       + "#SBATCH --job-name=" + identifier + "\n"
                       + "#SBATCH --nodes=" + nodes + "\n"
                       + "#SBATCH --ntasks-per-node=" + ntasks_per_node  + "\n"
                       + "#SBATCH --cpus-per-task=" + cpus_per_task + "\n\n"                       
                       + "source activate" + s + path_qiime + "\n\n" #"source activate" + s + path_qiime + "\n\n"
                       + "cd" + s + path[:-1] + "\n\n"
                       + "mkdir -p" + s + path + "temp" + "\n"   # "mkdir -p temp" + "\n"
                       + "export TMPDIR=" + path + "temp" + "\n\n"
                       + "mkdir -p" + s + identifier  + "\n\n" #"mkdir -p" + s + path + identifier + "\n\n"
                       + "mkdir -p" + s + identifier  + "/raw_data" + "\n\n"
                       + "qiime" + "\n\n"
                       + "cp" + s + "-u" + s + identifier + "*_bash_step_*.sh" + s + path + identifier + "/" + "\n" 
                       + "cd" + s + path + identifier + "\n")

    return bash_00_intro_qiime_scripts



def step_00a_intro_graphs (path, nodes, ntasks_per_node, cpus_per_task, identifier, s, path_qiime, path_python):
    bash_00a_intro_graphs = ("#!/bin/bash" + "\n"
                           + "#SBATCH --job-name=" + identifier + "\n"
                           + "#SBATCH --nodes=" + nodes + "\n"
                           + "#SBATCH --ntasks-per-node=" + ntasks_per_node  + "\n"
                           + "#SBATCH --cpus-per-task=" + cpus_per_task + "\n\n"                       
                           + "source activate" + s + path_qiime + "\n\n"
                           + "qiime" + "\n\n"
                           + "cd" + s + path[:-1] + "\n\n"
                           + "cp" + s + path_python + "qiime_settings.ini" + s + path + identifier + "/qiime_settings.txt" + "\n"
                           + "cp" + s + "-u" + s + path + identifier + "*_bash_step_*.sh" + s + path + identifier + "/" + "\n")

    return bash_00a_intro_graphs


def step_01_import (path, inputfile, identifier, s):
    bash_01_import = ('qiime tools import' + s + "\\" + "\n"
                        + '--type MultiplexedPairedEndBarcodeInSequence' + s + "\\" + "\n"
                        + '--input-path' + s + path + identifier + "/raw_data" + s + "\\" + "\n"
                        + '--output-path' + s + path + identifier + "/" + identifier + "_paired_end_sequences.qza" + "\n")
    return bash_01_import

#qiime tools import \
#--type MultiplexedPairedEndBarcodeInSequence \
#--input-path fastq_files/QIIME2_input_files \
#--output-path paired-end-sequences.qza

def step_02_demux (path, identifier, forward_barcodes_file, forward_barcodes_column, s):
    bash_02_demux = ("qiime cutadapt demux-paired" + s + "\\" + "\n"
                     + "--i-seqs" + s + path + identifier + "/" + identifier + "_paired_end_sequences.qza" + s + "\\" + "\n"
                     + "--m-forward-barcodes-file" + s + path + identifier + "/" + identifier + "@" + forward_barcodes_file + s + "\\" + "\n"
                     + "--m-forward-barcodes-column" + s + forward_barcodes_column  + s + "\\" + "\n"
                     + "--p-error-rate 0" + s + "\\" + "\n"
                     + "--o-per-sample-sequences" + s + path + identifier + "/" + identifier + "_demux.qza" + s + "\\" + "\n"
                     + "--o-untrimmed-sequences" + s + path + identifier + "/" + identifier + "_untrimmed.qza"  + s + "\\" + "\n"
                     + "--verbose" + "\n")

    return bash_02_demux


#qiime cutadapt demux-paired \
# --i-seqs paired-end-sequences.qza \
# --m-forward-barcodes-file metadata.txt \
# --m-forward-barcodes-column BarcodeSequence \
# --p-error-rate 0 \
# --o-per-sample-sequences demux.qza \
# --o-untrimmed-sequences untrimmed.qza \
# --verbose

def step_03_demuxsum (s, path, identifier):
    bash_03_demuxsum = ("qiime demux summarize" + s + "\\" + "\n"
                          + "--i-data" + s + path + identifier + "/" + identifier + "_demux.qza" + s + "\\" + "\n"
                          + "--o-visualization" + s + path + identifier + "/" + identifier + "_demux.qzv" + s + "\n")
    return bash_03_demuxsum


#qiime demux summarize \
#  --i-data demux.qza \
#  --o-visualization demux.qzv

##qiime tools view demux.qzv

def step_04_cutadapt (s, path, identifier, forward_primer, reverse_primer):
    bash_04_cutadapt = ("qiime cutadapt trim-paired" + s + "\\" + "\n"
                        + "--i-demultiplexed-sequences" + s+ path + identifier + "/" + identifier + "_demux.qza" + s + "\\" + "\n"
                        + "--p-front-f" + s + forward_primer + s + "\\" + "\n"
                        + "--p-front-r" + s + reverse_primer + s + "\\" + "\n"
                        + "--p-discard-untrimmed"  + s + "\\" + "\n"
                        + "--o-trimmed-sequences" + s + path + identifier + "/" + identifier + "_trimmed-demux-seqs.qza" + "\n")
    return bash_04_cutadapt 

#qiime cutadapt trim-paired \
#--i-demultiplexed-sequences demux.qza \
#--p-front-f GTGYCAGCMGCCGCGGTAA \
#--p-front-r CCGYCAATTYMTTTRAGTTT \
#--p-discard-untrimmed
#--o-trimmed-sequences trimmed-demux-seqs.qza \


def step_05_trimsum (s, path, identifier):
    bash_05_trimsum = ("qiime demux summarize" + s + "\\" + "\n"
                         + "--i-data" + s + path + identifier + "/" + identifier + "_trimmed-demux-seqs.qza" + s + "\\" + "\n"
                         + "--o-visualization" + s + path + identifier + "/" + identifier + "_trimmed-demux-seqs.qzv" + s + "\n")
    return bash_05_trimsum

def step_05b_copy_quality_sums (s, path, identifier, path_python):
    bash_05b_copy_quality_sums = ("unzip" + s + path + identifier + "/" + identifier + "_demux.qzv" + s + "-d" + s + path + identifier + "\n"
                                  + "find" + s + path + identifier + s + "-type f -name 'forward-seven-number-summaries.csv' -exec sh -c" + s + "'for arg do cp --" + s + '"$arg"' + s
                                  + '"' + path + identifier + "/" + identifier + "_forward-seven-number-summaries.csv" + '"' + "; done' _ {} +" + "\n"
                                  + "find" + s + path + identifier + s + "-type f -name 'reverse-seven-number-summaries.csv' -exec sh -c" + s + "'for arg do cp --" + s + '"$arg"' + s
                                  + '"' + path + identifier + "/" + identifier + "_reverse-seven-number-summaries.csv" + '"' + "; done' _ {} +" + "\n"
                                  # + "cp" + s + path + "quality_scores_datasets.txt" + s + path + identifier + "/" + identifier + "_quality_scores_datasets.txt" + "\n"
                                  + "unzip" + s + path + identifier + "/" + identifier + "_denoising_stats.qza" + s + "-d" + s + path + identifier + "\n"
                                  + "find" + s + path + identifier + s + "-type f -name 'stats.tsv' -exec sh -c" + s + "'for arg do cp --" + s + '"$arg"' + s
                                  + '"' + path + identifier + "/" + "CHECK_" + identifier + "_stats.tsv" + '"' + "; done' _ {} +" + "\n")
    
    return bash_05b_copy_quality_sums


def step_06_dada2 (s, path, identifier, trim_forward, trim_reverse, length_forward, length_reverse, cpus_per_task):
    bash_06_dada2 = ("qiime dada2 denoise-paired" + s + "\\" + "\n"
                     + "--i-demultiplexed-seqs" + s + path + identifier + "/" + identifier + "_trimmed-demux-seqs.qza" + s + "\\" + "\n"
                     + "--p-trim-left-f" + s + trim_forward + s + "\\" + "\n"
                     + "--p-trim-left-r" + s + trim_reverse + s + "\\" + "\n"
                     + "--p-trunc-len-f" + s + length_forward + s + "\\" + "\n"
                     + "--p-trunc-len-r" + s + length_reverse + s + "\\" + "\n"
                     #+ "--p-trunc-q" + s + trim_quality + s + "\\" + "\n"
                     + "--o-table" + s + path + identifier + "/" + identifier + "_table.qza" + s +  "\\" + "\n"
                     + "--o-representative-sequences" + s + path + identifier + "/" + identifier + "_representative_sequences.qza" + s + "\\" + "\n"
                     + "--o-denoising-stats" + s + path + identifier + "/" + identifier + "_denoising_stats.qza" + s + "\\" + "\n"
                     + "--p-n-threads" + s + cpus_per_task + s + "\n")
                     #+ "cd" + s + "./" + identifier + "\n")
    return bash_06_dada2




#qiime dada2 denoise-paired \
#  --i-demultiplexed-seqs trimmed-demux-seqs.qza \
#  --p-trim-left-f 5 \
#  --p-trim-left-r 5 \
#  --p-trunc-len-f 240 \
#  --p-trunc-len-r 240 \
#  --output-dir DADA2_out_test \
#  --p-n-threads 16

def step_07_metadata_tab (s, path, identifier): 
    bash_07_metadata_tab = ("qiime metadata tabulate" + s + "\\" + "\n"
                            + "--m-input-file" + s + path + identifier + "/" + identifier + "_denoising_stats.qza" + s + "\\" + "\n"
                            + "--o-visualization" + s + path + identifier + "/" + identifier + "_denoising_stats.qzv" + "\n")
    return bash_07_metadata_tab


# view denoising stats
#qiime metadata tabulate \
#  --m-input-file denoising_stats.qza \
#  --o-visualization denoising_stats.qzv

def step_08_feature_table_sum (s, identifier, path, forward_barcodes_file):
    bash_08_feature_table_sum = ("qiime feature-table summarize" + s + "\\" + "\n"
                                 + "--i-table" + s + path + identifier + "/" + identifier + "_table.qza" + s + "\\" + "\n"
                                 + "--m-sample-metadata-file" + s + path + identifier + "/" + identifier + "@" + forward_barcodes_file + s + "\\" + "\n"
                                 + "--o-visualization" + s + path + identifier + "/" + identifier + "_table.qzv" + "\n")
    return bash_08_feature_table_sum



# view generated feature table
#qiime feature-table summarize \
#  --i-table table.qza \
#  --m-sample-metadata-file ~/QIIME2_workshop/metadata.txt
#  --o-visualization table.qzv
  
#qiime tools view table.qzv


def step_09_representative_seqs (s, path, identifier): 
    bash_09_representative_seqs = ("qiime feature-table tabulate-seqs" + s + "\\" + "\n"
                                   + "--i-data" + s + path + identifier + "/" + identifier + "_representative_sequences.qza" + s + "\\" + "\n"
                                   + "--o-visualization" + s + path + identifier + "/" + identifier + "_representative_sequences.qzv" + "\n")
                                   #+ "cd.." + "\n")
    return bash_09_representative_seqs

# view representative sequences for each ASV
#qiime feature-table tabulate-seqs \
# --i-data representative_sequences.qza \
#  --o-visualization representative_sequences.qzv
#qiime tools view representative_sequences.qzv

def step_10_align_mafft (s, path, identifier, cpus_per_task):
    bash_10_align_mafft = ("qiime alignment mafft" + s + "\\" + "\n"
                           + "--i-sequences" + s + path + identifier + "/" + identifier + "_representative_sequences.qza" + s + "\\" + "\n"
                           + "--o-alignment" + s + path + identifier + "/" + identifier + "_aligned-rep-seqs.qza" + s + "\\" + "\n"
                           + "--p-n-threads" + s + cpus_per_task + s + "\n")
    return bash_10_align_mafft

#qiime alignment mafft \
#  --i-sequences DADA2_out/representative_sequences.qza \
#  --o-alignment aligned-rep-seqs.qza \
#  --p-n-threads 16


def step_11_align_mask (s, path, identifier):
    bash_11_align_mask = ("qiime alignment mask" + s + "\\" + "\n"
                          + "--i-alignment" + s + path + identifier + "/" + identifier + "_aligned-rep-seqs.qza" + s + "\\" + "\n"
                          + "--o-masked-alignment" + s + path + identifier + "/" + identifier + "_masked_aligned-rep-seqs.qza" + "\n")
    return bash_11_align_mask


#qiime alignment mask \
#  --i-alignment aligned-rep-seqs.qza \
#  --o-masked-alignment masked_aligned-rep-seqs.qza

def step_12_phyl_fast (s, path, identifier, cpus_per_task):
    bash_12_phyl_fast = ("qiime phylogeny fasttree" + s + "\\" + "\n"
                         + "--i-alignment" + s + path + identifier + "/" + identifier + "_masked_aligned-rep-seqs.qza" + s + "\\" + "\n"
                         + "--o-tree" + s + path + identifier + "/" + identifier + "_unrooted-tree.qza" + s + "\\" + "\n"
                         + "--p-n-threads" + s + cpus_per_task + "\n")
    return bash_12_phyl_fast

#qiime phylogeny fasttree \
#  --i-alignment masked_aligned-rep-seqs.qza \
#  --o-tree unrooted-tree.qza \
#  --p-n-threads 16


def step_13_phyl_mid (s, path, identifier):
    bash_13_phyl_mid = ("qiime phylogeny midpoint-root" + s + "\\" + "\n"
                          + "--i-tree" + s + path + identifier + "/" + identifier + "_unrooted-tree.qza" + s + "\\" + "\n"
                          + "--o-rooted-tree" + s + path + identifier + "/" + identifier + "_rooted-tree.qza" + "\n")
    return bash_13_phyl_mid
  
#qiime phylogeny midpoint-root \
#  --i-tree unrooted-tree.qza \
#  --o-rooted-tree rooted-tree.qza

def step_14_feature_class (s, path, identifier, classifier, cpus_per_task, path_classifier):
    bash_14_feature_class = ("qiime feature-classifier classify-sklearn" + s + "\\" + "\n"
                             + "--i-classifier" + s + path_classifier + classifier + s + "\\" + "\n"
                             + "--i-reads" + s + path + identifier + "/" + identifier + "_representative_sequences.qza" + s + "\\" + "\n"
                             + "--o-classification" + s + path + identifier + "/" + identifier + "_taxonomy_" + classifier + s + "\\" + "\n"
                             + "--p-n-jobs" + s + cpus_per_task + "\n")
    return bash_14_feature_class

#qiime feature-classifier classify-sklearn \
#  --i-classifier NB_classifier_SILVA_132_99_16S_V4-V5.qza \
#  --i-reads DADA2_out/representative_sequences.qza \
#  --o-classification taxonomy_Silva132_99-515F-926R_classifier.qza \
#  --p-n-jobs 16

def step_15_metadata_tab (s, path, identifier, classifier, classifier_0 ):
    bash_15_metadata_tab = ("qiime metadata tabulate" + s + "\\" + "\n"
                            + "--m-input-file" + s + path + identifier + "/" + identifier + "_taxonomy_" + classifier + s + "\\" + "\n"
                            + "--o-visualization" + s + path + identifier + "/" + identifier + "_taxonomy_" + classifier_0 + ".qzv" + "\n")
                            #+ "mkdir" + s + "/" + identifier + "_output_files" + "\n\n")
    return bash_15_metadata_tab


#qiime metadata tabulate \
#  --m-input-file taxonomy_SILVA_132_99_16S_V4-V5.qza \
#  --o-visualization taxonomy_SILVA_132_99_16S_V4-V5.qzv


def step_16_export_repr_seq_fasta (s, path, identifier):
    bash_16_export_repr_seq_fasta = ("qiime tools export" + s + "\\" + "\n"
                                     + "--input-path" + s + path + identifier + "/" + identifier + "_representative_sequences.qza" + s + "\\" + "\n"
                                     + "--output-path" + s + path + identifier + "\n")

    return bash_16_export_repr_seq_fasta

# export representative sequences as a .fasta file
#qiime tools export \
#  --input-path DADA2_out/representative_sequences.qza \
#  --output-path output_files/rep-seqs

def step_17_export_feat_tbl_biom (s, path, identifier):
    bash_17_export_feat_tbl_biom = ("qiime tools export" + s + "\\" + "\n"
                                    + "--input-path" + s + path + identifier + "/" + identifier + "_table.qza" + s + "\\" + "\n"
                                    + "--output-path" + s + path + identifier + "\n")


    return bash_17_export_feat_tbl_biom

# export feature table as .biom file
#qiime tools export \
#  --input-path DADA2_out/table.qza \
#  --output-path output_files/exported-table

def step_18_export_phyl_newick (s, path, identifier):
    bash_18_export_phyl_newick = ("qiime tools export" + s + "\\" + "\n"
                                    + "--input-path" + s + path + identifier + "/" + identifier + "_rooted-tree.qza" + s + "\\" + "\n"
                                    + "--output-path" + s + path + identifier +  "\n")

    return bash_18_export_phyl_newick

# export phylogeny as .nwk tree file in Newick format
#qiime tools export \
#  --input-path rooted-tree.qza \
#  --output-path output_files/exported-tree

def step_19_export_taxonomy_tsv (s, path, identifier, classifier):
    bash_19_export_taxonomy_tsv = ("qiime tools export" + s + "\\" + "\n"
                                    + "--input-path" + s + path + identifier + "/" + identifier + "_taxonomy_" + classifier + s + "\\" + "\n"
                                    + "--output-path" + s + path + identifier + "/" + "\n")

    return bash_19_export_taxonomy_tsv

def step_20_export_rename (s, path, identifier):
    bash_20_export_rename = ( "mv" + s + path + identifier + "/" + "dna-sequences.fasta" + s + path + identifier + "/" + identifier + "_dna-sequences.fasta" + "\n"
                              + "mv" + s + path + identifier + "/" + "feature-table.biom" + s + path + identifier + "/" + identifier + "_feature-table.biom" + "\n"
                              + "mv" + s + path + identifier + "/" + "tree.nwk" + s + path + identifier + "/" + identifier + "_tree.nwk" + "\n"
                              + "mv" + s + path + identifier + "/" + "taxonomy.tsv" + s + path + identifier + "/" + identifier + "_taxonomy.tsv" + "\n")

    return bash_20_export_rename
    



def step_21_alpha_rarefaction (s, path, identifier, forward_barcodes_file, min_depth, max_depth):
    bash_21_alpha_rarefaction = ("qiime diversity alpha-rarefaction" + s + "\\" + "\n"
                                 + "--i-table" + s + path + identifier + "/" + identifier + "_table.qza" + s +  "\\" + "\n"
                                 + "--m-metadata-file" + s + path + identifier + "/" + identifier + "@" + forward_barcodes_file + s + "\\" + "\n"
                                 + "--o-visualization" + s + path + identifier + "/" + identifier + "_alpha_rarefaction_curves.qzv" + s + "\\" + "\n"
                                 + "--p-min-depth" + s + min_depth + s + "\\" + "\n"
                                 + "--p-max-depth" + s + max_depth + "\n\n")
    return bash_21_alpha_rarefaction




#qiime diversity alpha-rarefaction \
#  --i-table DADA2_out/table.qza \
#  --m-metadata-file metadata.txt \
#  --o-visualization alpha_rarefaction_curves.qzv \
#  --p-min-depth 10 \
#  --p-max-depth xxx







def step_22_microbial_diversity (s, path, identifier, forward_barcodes_file, sampling_depth):
    bash_22_microbial_diversity = ("qiime diversity core-metrics-phylogenetic" + s + "\\" + "\n"
                                   + "--i-table" + s + path + identifier + "/" + identifier + "_table.qza" + s +  "\\" + "\n"
                                   + "--i-phylogeny" + s + path + identifier + "/" + identifier + "_rooted-tree.qza" + s + "\\" + "\n"
                                   + "--m-metadata-file" + s + path + identifier + "/" + identifier + "@" + forward_barcodes_file + s + "\\" + "\n"
                                   + "--p-sampling-depth" + s + sampling_depth + s + "\\" + "\n"
                                   + "--output-dir" + s + path + identifier + "/" + identifier + "_microbial-diversity-results" + "\n\n")
    return bash_22_microbial_diversity
                                   

#qiime diversity core-metrics-phylogenetic \
#  --i-table DADA2_out/table.qza \
#  --i-phylogeny rooted-tree.qza \
#  --m-metadata-file metadata.txt \
#  --p-sampling-depth 260 \
#  --output-dir microbial-diversity-results


def step_23_taxa_barplot (s, path, identifier, forward_barcodes_file, classifier):
    bash_23_taxa_barplot = ("qiime taxa barplot" + s + "\\" + "\n"
                            + "--i-table" + s + path + identifier + "/" + identifier + "_table.qza" + s +  "\\" + "\n"
                            + "--i-taxonomy" + s + path + identifier + "/" + identifier + "_taxonomy_" + classifier + s + "\\" + "\n"
                            + "--m-metadata-file" + s + path + identifier + "/" + identifier + "@" + forward_barcodes_file + s + "\\" + "\n"
                            + "--o-visualization" + s + path + identifier + "/" + identifier + "_taxa_barplot.qzv" + "\n\n")
    return bash_23_taxa_barplot
 

#qiime taxa barplot \
  #--i-table DADA2_out/table.qza \
  #--i-taxonomy taxonomy_Silva132_99-515F-926R_classifier_qiime2-2019.10.qza \
  #--m-metadata-file metadata.txt \
  #--o-visualization taxa_barplot.qzv

#qiime tools view taxa_barplot.qzv






file_list = set()



for inputfile in inputfiles: #RBAR_01_20200115@SAM1-17_S2_L001_R1_001.fastq
    item0 = inputfile.split("@")
    item  = item0[0] #RBAR_01_20200115
    file_list.add(item)

print (file_list)

for identifier in file_list:
        
    sbatchfile_00 = (identifier + "_bash_step_00_qiime_quality.sh") #(identifier + "_bash_step_01_qiime_scripts.sh")
    sbatch_00 = open(sbatchfile_00 , mode='wb+', newline = None)

    sbatchfile_01 = (identifier + "_bash_step_01_qiime_scripts.sh") #(identifier + "_bash_step_02_qiime_graphs.sh")
    sbatch_01 = open(sbatchfile_01 , mode='wb+', newline = None)

    sbatchfile_02 = (identifier + "_bash_step_02_qiime_graphs.sh") #(identifier + "_bash_step_00_qiime_quality.sh")
    sbatch_02 = open(sbatchfile_02 , mode='wb+', newline = None)

    #sbatchfile_03 = (identifier + "_bash_step_01b_qiime_subsets_repeat.sh")
    #sbatch_03 = open(sbatchfile_03 , mode='wb+', newline = None)



    #sbatchfile_02 = (identifier + "_q_man_02.sh")
    #sbatch_02 = open(sbatchfile_02 , mode='wb+', newline = None)
    

    #bash_00_intro = step_00_intro (path, nodes, ntasks_per_node, cpus_per_task, identifier, s, qiime_version, path_qiime, path_python, forward_barcodes_file)
    bash_00_intro_sub_quality = step_00_intro_sub_quality (path, nodes, ntasks_per_node, cpus_per_task, identifier, s, qiime_version, path_qiime, path_python, forward_barcodes_file, fastq_sub, name_sub)
    bash_00_intro_qiime_scripts =  step_00_intro_qiime_scripts (path, nodes, ntasks_per_node, cpus_per_task, identifier, s, qiime_version, path_qiime)
    bash_00a_intro_graphs = step_00a_intro_graphs (path, nodes, ntasks_per_node, cpus_per_task, identifier, s, path_qiime, path_python)
    bash_01_import = step_01_import (path, inputfile, identifier, s)
    bash_02_demux = step_02_demux (path, identifier, forward_barcodes_file, forward_barcodes_column, s)   
    bash_03_demuxsum = step_03_demuxsum (s, path, identifier)
    bash_04_cutadapt = step_04_cutadapt (s, path, identifier, forward_primer, reverse_primer)
    bash_05_trimsum = step_05_trimsum (s, path, identifier)    
    bash_06_dada2 = step_06_dada2 (s, path, identifier, trim_forward, trim_reverse, length_forward, length_reverse, cpus_per_task)
    bash_07_metadata_tab  = step_07_metadata_tab (s, path, identifier)
    bash_08_feature_table_sum = step_08_feature_table_sum (s, identifier, path, forward_barcodes_file)
    bash_09_representative_seqs = step_09_representative_seqs (s, path, identifier)
    bash_10_align_mafft = step_10_align_mafft (s, path, identifier, cpus_per_task)
    bash_11_align_mask = step_11_align_mask (s, path, identifier)
    bash_12_phyl_fast = step_12_phyl_fast (s, path, identifier, cpus_per_task)
    bash_13_phyl_mid = step_13_phyl_mid (s, path, identifier)
    bash_14_feature_class = step_14_feature_class (s, path, identifier, classifier, cpus_per_task, path_classifier)
    bash_15_metadata_tab = step_15_metadata_tab (s, path, identifier, classifier, classifier_0 )
    bash_16_export_repr_seq_fasta = step_16_export_repr_seq_fasta (s, path, identifier)
    bash_17_export_feat_tbl_biom = step_17_export_feat_tbl_biom (s, path, identifier)
    bash_18_export_phyl_newick = step_18_export_phyl_newick (s, path, identifier)
    bash_19_export_taxonomy_tsv = step_19_export_taxonomy_tsv (s, path, identifier, classifier)
    bash_20_export_rename = step_20_export_rename (s, path, identifier)
    bash_05b_copy_quality_sums = step_05b_copy_quality_sums (s, path, identifier, path_python)
    bash_21_alpha_rarefaction = step_21_alpha_rarefaction (s, path, identifier, forward_barcodes_file, min_depth, max_depth)
    bash_22_microbial_diversity = step_22_microbial_diversity (s, path, identifier, forward_barcodes_file, sampling_depth)
    bash_23_taxa_barplot = step_23_taxa_barplot (s, path, identifier, forward_barcodes_file, classifier)


    text_to_write_00 = (bash_00_intro_sub_quality + "\n" + "source deactivate" )

    text_to_write_01 = ( bash_00_intro_qiime_scripts + "\n" + bash_01_import + "\n" +  bash_02_demux + "\n"
                       + bash_03_demuxsum + "\n" + bash_04_cutadapt + "\n" + bash_05_trimsum + "\n"
                       + bash_06_dada2 + "\n" + bash_07_metadata_tab + "\n" + bash_08_feature_table_sum + "\n"
                       + bash_09_representative_seqs + "\n" + bash_10_align_mafft + "\n" + bash_11_align_mask + "\n"
                       + bash_12_phyl_fast + "\n" + bash_13_phyl_mid  + "\n" + bash_14_feature_class + "\n"
                       + bash_15_metadata_tab + "\n" + bash_16_export_repr_seq_fasta + "\n" + bash_17_export_feat_tbl_biom + "\n"
                       + bash_18_export_phyl_newick + "\n" + bash_19_export_taxonomy_tsv + "\n" + bash_20_export_rename + "\n"
                       + bash_05b_copy_quality_sums + "\n" + "source deactivate" )

    text_to_write_02 = ( bash_00a_intro_graphs + "\n" + bash_21_alpha_rarefaction + "\n" +  bash_22_microbial_diversity + "\n" + bash_23_taxa_barplot + "\n" + "source deactivate" )


    
                         #+ "\n" + bash_04_cutadapt + "\n" + bash_05_trimsum + "\n" + bash_05b_copy_quality_sums + "\n" + "source deactivate" )
    
    #text_to_write_2 =  ( bash_00_intro + "\n" + bash_06_dada2 + "\n" + bash_07_metadata_tab + "\n" + bash_08_feature_table_sum + "\n"
                       #+ bash_09_representative_seqs + "\n" + bash_10_align_mafft + "\n" + bash_11_align_mask + "\n"
                       #+ bash_12_phyl_fast + "\n" + bash_13_phyl_mid  + "\n" + bash_14_feature_class + "\n"
                       #+ bash_15_metadata_tab + "\n" + bash_16_export_repr_seq_fasta + "\n" + bash_17_export_feat_tbl_biom + "\n"
                       #+ bash_18_export_phyl_newick + "\n" + bash_19_export_taxonomy_tsv + "\n" + bash_20_export_rename + "\n" + bash_05b_copy_quality_sums + "\n" + "source deactivate" )

    #print(text_to_write_2)
    sbatch_00.write(bytes(text_to_write_00, "UTF-8"))

    sbatch_01.write(bytes(text_to_write_01, "UTF-8"))

    sbatch_02.write(bytes(text_to_write_02, "UTF-8"))

    #sbatch_03.write(bytes(text_to_write_3, "UTF-8"))


    sbatch_00.close()
    sbatch_01.close()
    sbatch_02.close()
    #sbatch_03.close()

# send = send
    #send = paramiko.SSHClient()
    #send.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
    #send.connect("192.168.192.209", port=22, username="bgeu", password="rc999", timeout = 4)  #p.connect("192.168.192.209", port=22, username="bgeu", password="rc999") ("192.168.1.198", port=22, username="pi", password="", timeout = 4)
    #sftp = send.open_sftp()
    #sftp.put(path_local + sbatchfile, path + sbatchfile)
    #sftp.put(path_local + sbatchfile_01, path + sbatchfile_01)
    #sftp.put(path_local + sbatchfile_02, path + sbatchfile_02)
    #sftp.close()

    #g1 = paramiko.SSHClient()
    #g1.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
    #g1.connect("192.168.192.209", port=22, username="bgeu", password="rc999", timeout = 4)  #p.connect("192.168.192.209", port=22, username="bgeu", password="rc999") ("192.168.1.198", port=22, username="pi", password="", timeout = 4)
    #sftp = g1.open_sftp()
    #sftp.get(path + identifier + "/" + identifier + "_forward-seven-number-summaries.csv" , path_local + "/" + identifier + "_forward-seven-number-summaries.csv")
    #sftp.get(path + identifier + "/" + identifier + "_reverse-seven-number-summaries.csv" , path_local + "/" + identifier + "_reverse-seven-number-summaries.csv")
    #sftp.close()




    print(identifier, " done")
print("BASH-scripts created")

