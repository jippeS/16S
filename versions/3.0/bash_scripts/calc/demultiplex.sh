#!/bin/bash
#SBATCH --output=Demultiplexing_%j.out
#SBATCH --job-name=Demultiplexing
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime cutadapt demux-paired --m-forward-barcodes-column BarcodeSequence --m-forward-barcodes-file $1 --i-seqs $2 --p-error-rate $3 --o-per-sample-sequences $4 --o-untrimmed-sequences $5 --verbose
