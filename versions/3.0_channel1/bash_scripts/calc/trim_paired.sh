#!/bin/bash
#SBATCH --output=trim_paired_%j.out
#SBATCH --partition=Superflex
#SBATCH --job-name=trim_paired
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --nodelist=flex3

qiime cutadapt trim-paired --i-demultiplexed-sequences $1 --p-front-f $2 --p-front-r $3 --p-discard-untrimmed --o-trimmed-sequences $4 --p-cores $5
