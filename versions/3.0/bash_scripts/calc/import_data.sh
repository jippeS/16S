#!/bin/bash
#SBATCH --output=Import_data_%j.out
#SBATCH --job-name=Import_data
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime tools import --type MultiplexedPairedEndBarcodeInSequence --input-path $1 --output-path $2
