import os
import pandas as pd
import configparser

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


#Classifier
path_classifier = config['qiime']['path_classifier']
classifier = config['qiime']['classifier'] #"silva-132-99-nb-classifier.qza" #"/export2/home/bgeu/qiime2_classifiers/NB_classifier_SILVA_132_99_16S_V4-V5_qiime2-2019.10.qza"  qiime2_classifiers


def create_folder_list (path):

    folder_names = list()

    os.system("cd " + path[:-1]) # + ";ls *.fastq.gz > " + path_python + "list_fastq_gz_files.txt")

    for entry_name in os.listdir(path[:-1]):
        entry_path = os.path.join(path[:-1], entry_name)
        if os.path.isdir(entry_path):
            folder_names.append(entry_name)

    print(folder_names)
    return (folder_names)


create_folder_list (path)
