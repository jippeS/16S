#!/bin/bash
#SBATCH --output=Import_data_%j.out
#SBATCH --job-name=Import_data
#SBATCH --partition=Superflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --nodelist=flex3

qiime tools import --type MultiplexedPairedEndBarcodeInSequence --input-path $1 --output-path $2
