#!/bin/bash
#SBATCH --job-name=trim_paired
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8

qiime cutadapt trim-paired \
--i-demultiplexed-sequences $1 \
--p-front-f $2 \
--p-front-r $3 \
--p-discard-untrimmed \
--o-trimmed-sequences $4
