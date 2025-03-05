#!/bin/bash
#SBATCH --output=Alignment_masking_%j.out
#SBATCH --job-name=Masking_alignment
#SBATCH --partition=Superflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --nodelist=flex3

qiime alignment mask --i-alignment $1 --o-masked-alignment $2
