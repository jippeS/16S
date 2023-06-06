#!/bin/bash
#SBATCH --output=denoise_paired_%j.out
#SBATCH --partition=Bytesflex
#SBATCH --job-name=Denois_pairing
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16


qiime dada2 denoise-paired --i-demultiplexed-seqs $1 --p-trim-left-f $2 --p-trim-left-r $3 --p-trunc-len-f $4 --p-trunc-len-r $5 --o-table  $6 --o-representative-sequences $7 --o-denoising-stats $8 --p-n-threads 16
