#!/bin/bash


if [ ! -f {output} ]; 
then 
    mkdir {config[inputdir]}input/;"
    mkdir {config[inputdir]}input/raw_data;"
    mkdir {config[inputdir]}tempdir;"
    unzip {config[inputdir]}*.zip -d {config[inputdir]}tempdir;"
     mv {config[inputdir]}tempdir/*.txt {config[inputdir]}input/{config[naming_convention]}@metadata.txt;"
     mv {config[inputdir]}tempdir/*/*_R1_*.fastq.gz {config[inputdir]}input/raw_data/forward1.fastq.gz;"
     mv {config[inputdir]}tempdir/*/*_R2_*.fastq.gz {config[inputdir]}input/raw_data/reverse1.fastq.gz;"
     gunzip -d {config[inputdir]}input/raw_data/forward1.fastq.gz;"
     gunzip -d {config[inputdir]}input/raw_data/reverse1.fastq.gz;"
     cp config.yaml {config[inputdir]}output/;"
     python3 python_scripts/pre_demux.py --inputdir={config[inputdir]};"
     gzip -c {config[inputdir]}input/raw_data/forward.fastq > {config[inputdir]}input/raw_data/forward.fastq.gz;"
     gzip -c {config[inputdir]}input/raw_data/reverse.fastq > {config[inputdir]}input/raw_data/reverse.fastq.gz;"
     rm {config[inputdir]}input/raw_data/*.fastq;"
     rm -rf {config[inputdir]}tempdir;"
     sbatch bash_scripts/calc/import_data.sh {params.inputpath}input/raw_data/ {output};"
     python3 {config[tooldir]}wetsus_packages/wait_file.py {output};
fi
