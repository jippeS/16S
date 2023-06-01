#!/bin/bash
#SBATCH --output=Alignment_masking_%j.out
#SBATCH --job-name=Masking_alignment
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime alignment mask --i-alignment $1 --o-masked-alignment $2
